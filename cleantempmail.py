"""Standard-library client for the CleanTempMail HTTP API (Python 3.10+)."""

import http.client
import json
import math
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Callable, Iterator

DEFAULT_BASE_URL = "https://cleantempmail.com/api"


class CleanTempMailError(Exception):
    """Base error; examples must not turn this into an empty inbox."""


class APIError(CleanTempMailError):
    """HTTP/API failure with quota and Retry-After information when available."""

    def __init__(self, message, *, status=None, usage=None, retry_after=None):
        self.status = status
        self.usage = usage
        self.retry_after = retry_after
        self.message = message
        super().__init__(f"HTTP {status}: {message}" if status else message)

    @property
    def quota_exhausted(self):
        usage = self.usage or {}
        exhausted = any(
            usage.get(f"{kind}_limit", 0) > 0
            and usage.get("remaining_today" if kind == "daily" else "remaining_total") == 0
            for kind in ("daily", "total")
        )
        return self.status == 429 and (
            exhausted or "quota" in self.message.lower()
        )

    @property
    def retryable(self):
        return not self.quota_exhausted and self.status in (429, 500, 502, 503, 504)


class TransportError(CleanTempMailError):
    """Connection or timeout failure; delivery of the request is uncertain."""


class _NoRedirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # urllib can copy custom headers to a redirect destination. Never
        # forward an API key or silently replay a request.
        return None


def _retry_after(value):
    if not value:
        return None
    try:
        seconds = float(value)
        return max(0.0, seconds) if math.isfinite(seconds) else None
    except ValueError:
        try:
            date = parsedate_to_datetime(value)
            if date.tzinfo is None:
                date = date.replace(tzinfo=timezone.utc)
            return max(0.0, (date - datetime.now(timezone.utc)).total_seconds())
        except (TypeError, ValueError, OverflowError):
            return None


class CleanTempMailClient:
    """Keys are sent only as X-API-Key, never in URLs or printed by the client.

    The transport does not replay requests: authenticated requests can consume
    quota even on failure. Only polling retries transient errors, with a deadline.
    """

    def __init__(self, api_key: str, base_url=DEFAULT_BASE_URL, timeout=15):
        if not api_key or not api_key.strip() or "\r" in api_key or "\n" in api_key:
            raise ValueError("A non-empty API key is required")
        parsed = urllib.parse.urlsplit(base_url)
        if (parsed.scheme not in ("https", "http") or not parsed.hostname
                or parsed.username or parsed.password or parsed.query or parsed.fragment):
            raise ValueError("base_url must be an HTTP(S) URL without credentials, query or fragment")
        if not math.isfinite(timeout) or timeout <= 0:
            raise ValueError("timeout must be positive and finite")
        self.api_key = api_key.strip()
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.last_usage = None
        self._opener = urllib.request.build_opener(_NoRedirects())

    @classmethod
    def from_env(cls):
        """Use the configured key, or the shared, limited ct-test demo key."""
        return cls(
            os.environ.get("CLEANTEMPMAIL_API_KEY", "ct-test"),
            os.environ.get("CLEANTEMPMAIL_BASE_URL", DEFAULT_BASE_URL),
        )

    def _redact(self, text):
        return text.replace(self.api_key, "[redacted]")

    def _open(self, endpoint, method="GET", data=None, *, auth=True, timeout=None):
        headers = {"Accept": "application/json", "User-Agent": "CleanTempMail-Python-Examples/2"}
        if auth:
            headers["X-API-Key"] = self.api_key
        body = None
        if data is not None:
            body = json.dumps(data).encode("utf-8")
            headers["Content-Type"] = "application/json"
        request = urllib.request.Request(
            self.base_url + endpoint, data=body, headers=headers, method=method,
        )
        try:
            return self._opener.open(request, timeout=self.timeout if timeout is None else timeout)
        except urllib.error.HTTPError as exc:
            with exc:
                raw = exc.read().decode("utf-8", errors="replace")
                try:
                    payload = json.loads(raw)
                except ValueError:
                    payload = {}
                if not isinstance(payload, dict):
                    payload = {}
                usage = payload.get("usage")
                if not isinstance(usage, dict):
                    usage = None
                if isinstance(usage, dict):
                    self.last_usage = usage
                message = payload.get("error") or raw[:300] or exc.reason
                raise APIError(
                    self._redact(str(message)), status=exc.code, usage=usage,
                    retry_after=_retry_after(exc.headers.get("Retry-After")),
                ) from None
        except (urllib.error.URLError, OSError, http.client.HTTPException) as exc:
            raise TransportError(self._redact(f"Network request failed: {exc}")) from None

    def _make_request(self, endpoint, method="GET", data=None, *, auth=True, timeout=None):
        try:
            with self._open(endpoint, method, data, auth=auth, timeout=timeout) as response:
                raw = response.read()
            payload = json.loads(raw)
        except (ValueError, UnicodeError):
            raise APIError("Server returned invalid JSON") from None
        except (OSError, urllib.error.URLError, http.client.HTTPException) as exc:
            raise TransportError(self._redact(f"Response read failed: {exc}")) from None
        if not isinstance(payload, dict):
            raise APIError("Server returned an unexpected response")
        if isinstance(payload.get("usage"), dict):
            self.last_usage = payload["usage"]
        if payload.get("success") is not True:
            raise APIError(self._redact(str(payload.get("error", "API request failed"))), usage=payload.get("usage"))
        if "data" not in payload:
            raise APIError("Server response has no data")
        return payload

    @staticmethod
    def _id(value):
        if not value:
            raise ValueError("An ID is required")
        return urllib.parse.quote(str(value), safe="")

    def get_domains(self, *, q=None, limit=1000, offset=0):
        """Public endpoint: returns domains, total, offset and limit; no quota."""
        if not 1 <= limit <= 2000 or offset < 0:
            raise ValueError("limit must be 1–2000; offset must be non-negative")
        params = {"limit": limit, "offset": offset}
        if q:
            params["q"] = q
        return self._make_request("/domains?" + urllib.parse.urlencode(params), auth=False)["data"]

    def generate_email(self, prefix=None, domain=None):
        data = {key: value for key, value in (("prefix", prefix), ("domain", domain)) if value is not None}
        response = self._make_request("/generate-email", "POST", data) if data else self._make_request("/generate-email")
        return response["data"]["email"]

    def get_emails(self, email_address, *, summary=False, _timeout=None):
        if not email_address:
            raise ValueError("An email address is required")
        params = {"email": email_address}
        if summary:
            params["summary"] = "1"
        return self._make_request("/emails?" + urllib.parse.urlencode(params), timeout=_timeout)["data"]["emails"]

    def get_email(self, email_id):
        return self._make_request("/email/" + self._id(email_id))["data"]

    def download_attachment(self, email_id, attachment_id):
        """Return bytes. The caller chooses the output path, not email metadata."""
        endpoint = f"/email/{self._id(email_id)}/attachment/{self._id(attachment_id)}"
        try:
            with self._open(endpoint) as response:
                return response.read()
        except (OSError, urllib.error.URLError, http.client.HTTPException) as exc:
            raise TransportError(self._redact(f"Attachment read failed: {exc}")) from None

    def delete_email(self, email_id):
        self._make_request("/email/" + self._id(email_id), "DELETE")
        return True

    def clear_inbox(self, email_address):
        if not email_address:
            raise ValueError("An email address is required")
        params = urllib.parse.urlencode({"email": email_address})
        return self._make_request("/emails/clear?" + params, "DELETE")["data"]["count"]

    def get_usage(self):
        """Query even an exhausted key; this POST does not consume quota."""
        return self._make_request("/api-key/usage", "POST")["data"]

    def get_statistics(self):
        return self._make_request("/stats")["data"]

    def get_24h_distribution(self):
        return self._make_request("/statistics/24h")["data"]

    def _top(self, kind, limit):
        if not 1 <= limit <= 10:
            raise ValueError("Statistics return at most 10 entries")
        return self._make_request("/statistics/top-" + kind)["data"][:limit]

    def get_top_subjects(self, limit=10):
        return self._top("subjects", limit)

    def get_top_domains(self, limit=10):
        return self._top("domains", limit)

    def get_top_senders(self, limit=10):
        return self._top("senders", limit)

    def iter_new_emails(self, email_address, *, timeout=120, interval=10, seen_ids=None) -> Iterator[dict]:
        """Yield each unseen summary once, including existing mail by default.

        A summary has a short text preview, not a full body; use get_email(id)
        for complete content. Pass seen_ids to ignore previously read messages.
        """
        if not all(math.isfinite(value) and value > 0 for value in (timeout, interval)):
            raise ValueError("timeout and interval must be positive and finite")
        seen = set(seen_ids or ())
        deadline = time.monotonic() + timeout
        failures = 0
        while (remaining := deadline - time.monotonic()) > 0:
            delay = interval
            try:
                messages = self.get_emails(email_address, summary=True, _timeout=min(self.timeout, remaining))
                failures = 0
            except (APIError, TransportError) as exc:
                if isinstance(exc, APIError) and not exc.retryable:
                    raise
                failures += 1
                if failures >= 3:
                    raise
                delay = max(interval * 2 ** failures, getattr(exc, "retry_after", None) or 0)
                if delay >= deadline - time.monotonic():
                    raise
            else:
                for message in messages:
                    if message["id"] not in seen:
                        seen.add(message["id"])
                        yield message
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                return
            time.sleep(min(delay, remaining))

    def wait_for_email(self, email_address, timeout=120, interval=10, *, seen_ids=None,
                       predicate: Callable[[dict], bool] | None = None):
        """Return a matching summary or None. Check immediately before sleeping."""
        for message in self.iter_new_emails(email_address, timeout=timeout, interval=interval, seen_ids=seen_ids):
            if predicate is None or predicate(message):
                return message
        return None


if __name__ == "__main__":
    from example_helpers import run
    run(lambda: print(json.dumps(CleanTempMailClient.from_env().get_usage(), indent=2)))
