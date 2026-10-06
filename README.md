# CleanTempMail API — Python examples

[English](README.md) | [简体中文](README_CN.md) | [Français](README_FR.md) | [日本語](README_JA.md) | [한국어](README_KO.md) | [Español](README_ES.md)

Official examples and a small reusable client for the [CleanTempMail API](https://cleantempmail.com/api): create temporary addresses, receive messages, extract verification codes and download attachments for tests of your own application.

**Python 3.10+ · standard library only · MIT license**

## Setup

```bash
git clone https://github.com/cleantempmail/cleantempmail-python-examples.git
cd cleantempmail-python-examples
export CLEANTEMPMAIL_API_KEY='YOUR_API_KEY'
python3 11_key_usage.py
python3 demo.py
```

PowerShell: `$env:CLEANTEMPMAIL_API_KEY = 'YOUR_API_KEY'`.
No `pip install` is needed, including for the async example. The default API base is `https://cleantempmail.com/api`; `CLEANTEMPMAIL_BASE_URL` can override it for a self-hosted deployment. Use HTTPS outside local development. See [.env.example](.env.example); the scripts read environment variables and **do not automatically load `.env` files**.

## Keys, payment and request accounting

- Buy a key at [API pricing and documentation](https://cleantempmail.com/api). Purchased keys have a fixed total request allowance, are paid once, do not auto-renew and cannot be topped up. Refer to the website for current plans and prices.
- Without `CLEANTEMPMAIL_API_KEY`, examples use **`ct-test`**, a shared, limited demo key. Everyone shares its allowance; it may already be exhausted. It is not a production credential or a promise of unlimited free API access.
- The client sends keys in `X-API-Key`. Keep production keys out of code, Git, URLs, logs and screenshots. Redirects are rejected rather than forwarding the key.
- Every authenticated protected request consumes **1 request**, including an empty inbox poll, reading a message, an attachment download, delete/clear and statistics calls with a key. Quota is reserved before the endpoint runs; a failed or retried request can also consume it.
- `POST /api/api-key/usage` checks the key without consuming its allowance. `GET /api/domains` is public; this client omits the key on that request. Public statistics can also be requested without a key, but this client's statistics methods send the key and consume quota.
- `remaining_total` is the lifetime balance; `remaining_today` is the daily balance. A limit of `0` and remaining value of `-1` mean unlimited for that dimension. This does not remove server rate or concurrency limits.
- Quota and request frequency are different. Rate limits may change with server configuration and can apply to both the key and the source IP. Honor `Retry-After`; do not assume a purchased key removes rate limits.

## Quick start

```python
from cleantempmail import CleanTempMailClient

client = CleanTempMailClient.from_env()
print(client.get_usage())                    # no quota charge
address = client.generate_email()           # 1 request
print(address)                              # send a test message to this address
message = client.wait_for_email(address, timeout=120, interval=10)
if message:
    full = client.get_email(message["id"])   # 1 additional request
    print(full["subject"], full["content"])
print(client.last_usage)                    # snapshot from the last charged JSON response
```

`wait_for_email()` checks immediately, then polls at the requested interval. It includes mail already in the inbox, so a message arriving before the helper starts is not missed. Pass `seen_ids={...}` to ignore old IDs, and optionally `predicate=lambda message: ...` to select a subject or sender. A successful wait returns a **summary**, not a complete message. No message before the deadline returns `None`; terminal API failures raise an exception.

Polling requests use `summary=1`: up to 100 recent messages with a short text preview. `get_emails(address)` without `summary=True` returns up to 500 recent complete messages. Use `get_email(id)` for the full body of a summary. These are retained messages, not an archive; messages and attachment IDs expire according to the service's retention settings.

## Examples

| Script | Run / purpose |
| --- | --- |
| [demo.py](demo.py) | `python3 demo.py`; opt-in monitoring: `python3 demo.py --wait` |
| [01_generate_email.py](01_generate_email.py) | Generate one random address |
| [02_custom_email.py](02_custom_email.py) | `python3 02_custom_email.py --prefix qa.user`; chooses an active domain |
| [03_receive_email.py](03_receive_email.py) | `python3 03_receive_email.py 'ADDRESS'`; read full inbox messages |
| [04_auto_polling.py](04_auto_polling.py) | `python3 04_auto_polling.py 'ADDRESS' --timeout 120 --interval 10` |
| [05_delete_email.py](05_delete_email.py) | `python3 05_delete_email.py 'MESSAGE_ID' --yes`; permanent deletion |
| [06_clear_inbox.py](06_clear_inbox.py) | `python3 06_clear_inbox.py 'ADDRESS' --yes`; permanent inbox cleanup |
| [07_statistics.py](07_statistics.py) | Get overview, hourly distribution and top subjects/domains/senders (5 requests) |
| [08_async_client.py](08_async_client.py) | Generate 3 addresses with `asyncio.to_thread` (3 requests) |
| [09_verification_code.py](09_verification_code.py) | `python3 09_verification_code.py 'ADDRESS' --keyword verification` |
| [10_multiple_addresses.py](10_multiple_addresses.py) | `python3 10_multiple_addresses.py --count 3`; generate and inspect a few inboxes |
| [11_key_usage.py](11_key_usage.py) | Query key status and remaining daily/total quota |
| [12_download_attachment.py](12_download_attachment.py) | `python3 12_download_attachment.py 'MESSAGE_ID' 'ATTACHMENT_ID' ./receipt.pdf` |
| [13_list_domains.py](13_list_domains.py) | Paginate current public domains; optional `--query` filter |
| [example_client.py](example_client.py) | Basic reusable-client usage |

The demo never deletes mail. Deletion scripts send no request without `--yes`. The attachment script uses a caller-chosen output path and refuses to overwrite an existing file. Code extraction is heuristic; adapt its patterns to the mail format in your test. HTML is parsed locally as text without loading images or other remote resources.

## HTTP API reference

All JSON endpoints use `{"success": true, "data": ...}` or `{"success": false, "error": "..."}`. Protected responses can include `usage`. Inbox lists contain `data.emails` and `data.count`. A message uses `id`, `email_address`, `from_address`, `subject`, `content`, `html_content`, `has_html`, `timestamp` (Unix seconds) and optional `attachments` metadata.

| Method | Path relative to the API base | Client method |
| --- | --- | --- |
| GET | `/domains?q=...&limit=1000&offset=0` | `get_domains(q=..., limit=..., offset=...)` → page dict |
| GET / POST | `/generate-email` | `generate_email(prefix=None, domain=None)` → address |
| GET | `/emails?email=...` | `get_emails(address, summary=False)` → list |
| GET | `/email/{id}` | `get_email(id)` → message dict |
| GET | `/email/{id}/attachment/{attachmentID}` | `download_attachment(id, attachment_id)` → bytes |
| DELETE | `/email/{id}` | `delete_email(id)` → `True` on success |
| DELETE | `/emails/clear?email=...` | `clear_inbox(address)` → deleted count |
| POST | `/api-key/usage` | `get_usage()` → status and quota dict |
| GET | `/stats` | `get_statistics()` → dict |
| GET | `/statistics/24h` | `get_24h_distribution()` → list |
| GET | `/statistics/top-subjects` | `get_top_subjects(limit=10)` → list |
| GET | `/statistics/top-domains` | `get_top_domains(limit=10)` → list |
| GET | `/statistics/top-senders` | `get_top_senders(limit=10)` → list |

Custom generation uses a JSON POST, for example `{"prefix": "qa.user", "domain": "ACTIVE_DOMAIN"}`. Domains change: get them from `get_domains()` rather than hardcoding an old one. An unavailable explicitly selected domain returns **HTTP 409**, rather than silently generating a different address. Private GPTMail domains are not accessible through this API. An address can also be constructed locally from a valid prefix and active public domain without a generation request; that does not reserve an inbox or make it private.

The attachment endpoint returns raw bytes, **not JSON**, and can return plain-text errors. Use `attachments[].id` from a complete message to fetch a file. Do not automatically open email links or execute downloaded files.

## Errors, timeouts and retries

```python
from cleantempmail import APIError, TransportError

try:
    messages = client.get_emails(address)
except APIError as error:
    print(error.status, error.message)
    print(error.usage, error.retry_after)
    if error.quota_exhausted:
        # No immediate retry: use another key, or wait for a daily reset.
        pass
except TransportError as error:
    print(error)  # connection or timeout error; request outcome may be unknown
```

| Status | Handling |
| --- | --- |
| 400 | Fix the request; do not retry unchanged. |
| 401 | Missing, invalid or inactive key; check the credential. |
| 403 | Private/forbidden inbox; do not retry through this API. |
| 404 | Message/attachment absent or expired; refresh IDs. |
| 409 | Selected domain unavailable; deliberately choose a current domain. |
| 429 | Distinguish exhausted quota from temporary rate limiting. Quota exhaustion stops polling; temporary limits use `Retry-After` and backoff. |
| 5xx | Temporary upstream failure or overload; bounded retries may help. |

`CleanTempMailClient(key, timeout=15)` sets an HTTP timeout. Ordinary calls are made once; they do not retry generation/deletion or hide a failure as `[]`. Polling retries transient 429/500/502/503/504 and transport failures with backoff, respects `Retry-After`, and raises after 3 consecutive failures or when there is no time to retry. Its per-request timeout is capped by the monitoring deadline. Each retry can cost another request. HTTP redirects are not followed.

## Checks and contributions

```bash
python3 -m unittest discover -s tests -v
python3 -m compileall -q .
```

Tests use a local mock API and synthetic emails. GitHub Actions runs them on Python 3.10–3.14 without credentials or live inbox access. See [CONTRIBUTING.md](CONTRIBUTING.md).

[Website](https://cleantempmail.com) · [Current API documentation and pricing](https://cleantempmail.com/api) · [Issues](https://github.com/cleantempmail/cleantempmail-python-examples/issues) · [MIT license](LICENSE)
