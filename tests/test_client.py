import importlib.util
import json
import os
import subprocess
import sys
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit

from cleantempmail import APIError, CleanTempMailClient, TransportError, _retry_after

ROOT = Path(__file__).resolve().parents[1]
KEY = "synthetic-test-key"
USAGE = {"daily_limit": 0, "used_today": 2, "remaining_today": -1,
         "total_limit": 100, "total_used": 2, "remaining_total": 98}
MESSAGE = {"id": "mail-1", "email_address": "qa@example.test", "from_address": "sender@example.test",
           "subject": "Your code", "content": "Your code is 123456", "html_content": "<p>123456</p>",
           "timestamp": 1787702400, "has_html": True,
           "attachments": [{"id": "file-1", "filename": "receipt.pdf", "size": 5, "content_type": "application/pdf"}]}


class MockAPI(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def handle_request(self):
        body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        self.server.records.append((self.command, self.path, dict(self.headers), body))
        if self.server.reply is not None:
            status, payload, headers = self.server.reply
        else:
            path = urlsplit(self.path).path
            query = parse_qs(urlsplit(self.path).query)
            if path == "/api/domains":
                data = {"domains": ["example.test"], "total": 1, "offset": 0, "limit": 1}
            elif path == "/api/generate-email":
                request = json.loads(body) if body else {}
                if request.get("domain") == "unavailable.invalid":
                    self.send_payload(409, {"success": False, "error": "Selected domain is unavailable"}, {})
                    return
                data = {"email": request.get("prefix", "random") + "@example.test"}
            elif path == "/api/emails":
                data = {"emails": [MESSAGE], "count": 1}
                if query.get("email") == ["empty@example.test"]:
                    data = {"emails": [], "count": 0}
            elif path == "/api/email/mail-1/attachment/file-1":
                self.send_payload(200, b"%PDF\x00", {"Content-Type": "application/pdf"})
                return
            elif path == "/api/email/mail-1":
                data = {"message": "Email deleted"} if self.command == "DELETE" else MESSAGE
            elif path == "/api/emails/clear":
                data = {"message": "Deleted 1 emails", "count": 1}
            elif path == "/api/api-key/usage":
                data = {**USAGE, "masked_key": "••••key", "status": "active", "is_active": True}
            elif path == "/api/stats":
                data = {"total_emails": 10, "active_domains": 1}
            elif path.startswith("/api/statistics/"):
                data = [{"count": 2}, {"count": 1}]
            else:
                self.send_payload(404, "Attachment not found", {})
                return
            status, payload, headers = 200, {"success": True, "data": data}, {}
            if self.headers.get("X-API-Key") and path not in ("/api/api-key/usage", "/api/domains"):
                payload["usage"] = USAGE
        self.send_payload(status, payload, headers)

    def send_payload(self, status, payload, headers):
        if isinstance(payload, (dict, list)):
            raw = json.dumps(payload).encode()
            content_type = "application/json"
        else:
            raw = payload.encode() if isinstance(payload, str) else payload
            content_type = "text/plain"
        self.send_response(status)
        self.send_header("Content-Type", headers.get("Content-Type", content_type))
        self.send_header("Content-Length", headers.get("Content-Length", str(len(raw))))
        for key, value in headers.items():
            if key not in ("Content-Type", "Content-Length"):
                self.send_header(key, value)
        self.end_headers()
        self.wfile.write(raw)

    do_GET = handle_request
    do_POST = handle_request
    do_DELETE = handle_request


class HTTPContractTests(unittest.TestCase):
    def setUp(self):
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), MockAPI)
        self.server.records = []
        self.server.reply = None
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.base = f"http://127.0.0.1:{self.server.server_port}/api"
        self.client = CleanTempMailClient(KEY, self.base, timeout=2)

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()

    def test_generation_uses_header_and_post_json(self):
        self.assertEqual(self.client.generate_email(), "random@example.test")
        self.assertEqual(self.client.generate_email(prefix="qa.user", domain="example.test"), "qa.user@example.test")
        method, path, headers, body = self.server.records[-1]
        self.assertEqual(method, "POST")
        self.assertNotIn(KEY, path)
        self.assertEqual(headers["X-Api-Key"], KEY)
        self.assertEqual(json.loads(body), {"prefix": "qa.user", "domain": "example.test"})
        self.assertEqual(self.client.last_usage, USAGE)

    def test_domain_pagination_omits_key(self):
        self.assertEqual(self.client.get_domains(q="example", limit=1, offset=0)["total"], 1)
        _, path, headers, _ = self.server.records[-1]
        self.assertEqual(parse_qs(urlsplit(path).query), {"q": ["example"], "limit": ["1"], "offset": ["0"]})
        self.assertNotIn("X-Api-Key", headers)

    def test_full_summary_detail_and_empty_inbox(self):
        self.assertEqual(self.client.get_emails("qa+test@example.test"), [MESSAGE])
        self.assertIn("qa%2Btest%40example.test", self.server.records[-1][1])
        self.client.get_emails("qa@example.test", summary=True)
        self.assertIn("summary=1", self.server.records[-1][1])
        self.assertEqual(self.client.get_email("mail-1"), MESSAGE)
        self.assertEqual(self.client.get_emails("empty@example.test"), [])

    def test_usage_is_post_header_without_body(self):
        self.assertEqual(self.client.get_usage()["remaining_total"], 98)
        method, path, headers, body = self.server.records[-1]
        self.assertEqual((method, path, body), ("POST", "/api/api-key/usage", b""))
        self.assertEqual(headers["X-Api-Key"], KEY)

    def test_delete_clear_and_statistics(self):
        self.assertTrue(self.client.delete_email("mail-1"))
        self.assertEqual(self.server.records[-1][0], "DELETE")
        self.assertEqual(self.client.clear_inbox("qa@example.test"), 1)
        self.assertEqual(self.client.get_statistics()["total_emails"], 10)
        self.assertEqual(len(self.client.get_24h_distribution()), 2)
        for method in (self.client.get_top_subjects, self.client.get_top_domains, self.client.get_top_senders):
            self.assertEqual(method(limit=1), [{"count": 2}])

    def test_binary_attachment_and_plain_text_error(self):
        self.assertEqual(self.client.download_attachment("mail-1", "file-1"), b"%PDF\x00")
        with self.assertRaises(APIError) as caught:
            self.client.download_attachment("mail-1", "missing")
        self.assertEqual(caught.exception.status, 404)
        self.assertEqual(caught.exception.message, "Attachment not found")

    def test_unavailable_domain_does_not_fall_back(self):
        with self.assertRaises(APIError) as caught:
            self.client.generate_email(domain="unavailable.invalid")
        self.assertEqual(caught.exception.status, 409)
        self.assertEqual(len(self.server.records), 1)

    def test_error_usage_retry_after_and_redaction(self):
        self.server.reply = (429, {"success": False, "error": f"Too many requests for {KEY}", "usage": USAGE}, {"Retry-After": "5"})
        with self.assertRaises(APIError) as caught:
            self.client.get_emails("qa@example.test")
        error = caught.exception
        self.assertNotIn(KEY, str(error))
        self.assertEqual(error.retry_after, 5)
        self.assertTrue(error.retryable)
        self.assertFalse(error.quota_exhausted)
        self.assertEqual(error.usage, USAGE)
        self.assertEqual(self.client.last_usage, USAGE)
        self.assertEqual(len(self.server.records), 1)  # ordinary calls do not retry

    def test_redirect_does_not_forward_key(self):
        self.server.reply = (302, "Moved", {"Location": self.base + "/foreign"})
        with self.assertRaises(APIError) as caught:
            self.client.generate_email()
        self.assertEqual(caught.exception.status, 302)
        self.assertEqual(len(self.server.records), 1)

    def test_invalid_and_unsuccessful_json_are_errors(self):
        for payload in ("<html>upstream failed</html>", [], {"success": False, "error": "Failure"}, {"success": True}):
            with self.subTest(payload=payload):
                self.server.reply = (200, payload, {})
                with self.assertRaises(APIError):
                    self.client.get_emails("qa@example.test")

    def test_truncated_response_is_transport_error(self):
        self.server.reply = (200, b"{}", {"Content-Length": "30"})
        with self.assertRaises(TransportError):
            self.client.get_usage()

    def test_demo_and_async_run_against_mock(self):
        env = {**os.environ, "CLEANTEMPMAIL_API_KEY": KEY, "CLEANTEMPMAIL_BASE_URL": self.base}
        for script in ("demo.py", "08_async_client.py", "example_client.py", "07_statistics.py"):
            with self.subTest(script=script):
                result = subprocess.run([sys.executable, str(ROOT / script)], env=env, capture_output=True, text=True, timeout=10)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertNotIn(KEY, result.stdout + result.stderr)
        self.assertFalse(any(method == "DELETE" for method, *_ in self.server.records))

    def test_failure_exit_is_not_empty_inbox(self):
        self.server.reply = (500, {"success": False, "error": "Failed to get emails"}, {})
        env = {**os.environ, "CLEANTEMPMAIL_API_KEY": KEY, "CLEANTEMPMAIL_BASE_URL": self.base}
        result = subprocess.run([sys.executable, str(ROOT / "03_receive_email.py"), "qa@example.test"], env=env, capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 1)
        self.assertIn("HTTP 500", result.stderr)
        self.assertNotIn("Inbox is empty", result.stdout)

    def test_deletion_scripts_require_confirmation(self):
        env = {**os.environ, "CLEANTEMPMAIL_API_KEY": KEY, "CLEANTEMPMAIL_BASE_URL": self.base}
        for script in ("05_delete_email.py", "06_clear_inbox.py"):
            result = subprocess.run([sys.executable, str(ROOT / script), "synthetic"], env=env, capture_output=True, text=True, timeout=10)
            self.assertEqual(result.returncode, 2)
        self.assertEqual(self.server.records, [])


class Clock:
    def __init__(self):
        self.now = 0
        self.sleeps = []

    def monotonic(self):
        return self.now

    def sleep(self, value):
        self.sleeps.append(value)
        self.now += value


class PollingTests(unittest.TestCase):
    def setUp(self):
        self.client = CleanTempMailClient(KEY)
        self.clock = Clock()
        self.patches = [patch("cleantempmail.time.monotonic", self.clock.monotonic),
                        patch("cleantempmail.time.sleep", self.clock.sleep)]
        for item in self.patches:
            item.start()
            self.addCleanup(item.stop)

    def test_immediate_arrival_is_not_lost(self):
        with patch.object(self.client, "get_emails", return_value=[MESSAGE]) as get:
            self.assertEqual(self.client.wait_for_email("qa@example.test"), MESSAGE)
            self.assertEqual(get.call_count, 1)
            self.assertTrue(get.call_args.kwargs["summary"])
            self.assertEqual(self.clock.sleeps, [])

    def test_ignore_old_mail_filter_and_suppress_duplicates(self):
        new = {**MESSAGE, "id": "mail-2", "subject": "Wanted"}
        with patch.object(self.client, "get_emails", side_effect=[[MESSAGE], [MESSAGE, new], [new]]):
            found = list(self.client.iter_new_emails("qa@example.test", timeout=25, interval=10, seen_ids={"mail-1"}))
            self.assertEqual(found, [new])
        self.clock.now = 0
        with patch.object(self.client, "get_emails", return_value=[MESSAGE, new]):
            self.assertEqual(self.client.wait_for_email("qa@example.test", predicate=lambda item: item["subject"] == "Wanted"), new)

    def test_empty_inbox_deadline_caps_each_http_timeout(self):
        with patch.object(self.client, "get_emails", return_value=[]) as get:
            self.assertIsNone(self.client.wait_for_email("qa@example.test", timeout=25, interval=10))
            self.assertEqual(get.call_count, 3)
            self.assertEqual(get.call_args.kwargs["_timeout"], 5)
            self.assertEqual(self.clock.now, 25)

    def test_rate_limit_respects_retry_after(self):
        error = APIError("Too many requests", status=429, retry_after=25)
        with patch.object(self.client, "get_emails", side_effect=[error, [MESSAGE]]):
            self.assertEqual(self.client.wait_for_email("qa@example.test", timeout=60), MESSAGE)
            self.assertEqual(self.clock.sleeps, [25])

    def test_daily_and_lifetime_quota_stop_without_retry(self):
        for usage in ({"daily_limit": 100, "remaining_today": 0}, {"total_limit": 100, "remaining_total": 0}):
            with self.subTest(usage=usage):
                error = APIError("Allowance exhausted", status=429, usage=usage)
                with patch.object(self.client, "get_emails", side_effect=error) as get:
                    with self.assertRaises(APIError):
                        self.client.wait_for_email("qa@example.test")
                    self.assertEqual(get.call_count, 1)
        self.assertEqual(self.clock.sleeps, [])

    def test_terminal_and_repeated_errors_are_not_timeouts(self):
        for error in (APIError("Private", status=403), TransportError("Offline"), APIError("Busy", status=503)):
            self.clock.now = 0
            with self.subTest(error=error):
                with patch.object(self.client, "get_emails", side_effect=error) as get:
                    with self.assertRaises(type(error)):
                        self.client.wait_for_email("qa@example.test")
                    self.assertEqual(get.call_count, 1 if isinstance(error, APIError) and error.status == 403 else 3)

    def test_failure_at_deadline_is_not_reported_as_no_mail(self):
        with patch.object(self.client, "get_emails", side_effect=APIError("Busy", status=503, retry_after=100)) as get:
            with self.assertRaises(APIError):
                self.client.wait_for_email("qa@example.test", timeout=20)
            self.assertEqual(get.call_count, 1)

    def test_invalid_config_fails_before_network(self):
        for value in (0, -1, float("inf")):
            with self.assertRaises(ValueError):
                self.client.wait_for_email("qa@example.test", interval=value)
            with self.assertRaises(ValueError):
                CleanTempMailClient(KEY, timeout=value)
        with self.assertRaises(ValueError):
            CleanTempMailClient(KEY, "https://example.test/api?api_key=secret")

    def test_retry_after_formats(self):
        self.assertEqual(_retry_after("5"), 5)
        self.assertEqual(_retry_after("Wed, 01 Jan 2020 00:00:00 GMT"), 0)
        self.assertIsNone(_retry_after("invalid"))
        self.assertIsNone(_retry_after("nan"))


class ExampleTests(unittest.TestCase):
    def test_code_extraction_and_html_without_remote_fetch(self):
        spec = importlib.util.spec_from_file_location("codes", ROOT / "09_verification_code.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertEqual(module.extract_codes("Your code is 123456. Again: 123456"), ["123456"])
        self.assertEqual(module.extract_codes("Security code: A12B34"), ["A12B34"])
        parser = module._TextOnly()
        parser.feed('<script>bad1234</script><style>bad5678</style><p>Code: 654321</p><img src="https://tracker.invalid">')
        self.assertEqual(module.extract_codes(" ".join(parser.parts)), ["654321"])

    def test_readme_links_resolve_and_no_external_python_imports(self):
        import ast
        import re
        for file in ROOT.glob("*.md"):
            for target in re.findall(r"\]\(([^)]+)\)", file.read_text()):
                if "://" not in target and not target.startswith("#"):
                    self.assertTrue((ROOT / target.split("#")[0]).exists(), f"{file.name}: missing {target}")
        for file in ROOT.glob("*.py"):
            tree = ast.parse(file.read_text(), filename=file.name, feature_version=(3, 10))
            for node in ast.walk(tree):
                names = [item.name for item in node.names] if isinstance(node, ast.Import) else [node.module] if isinstance(node, ast.ImportFrom) else []
                for name in names:
                    root_name = name.split(".")[0]
                    self.assertTrue(root_name in sys.stdlib_module_names or root_name in ("cleantempmail", "example_helpers"), f"{file.name}: {name}")


if __name__ == "__main__":
    unittest.main()
