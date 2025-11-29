# CleanTempMail API - Python Examples

[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

English | [简体中文](README_CN.md)

Official Python examples for [CleanTempMail](https://cleantempmail.com) - a free temporary email service with powerful API.

## 🚀 Features

- **Generate temporary emails** instantly
- **Receive emails** in real-time
- **Access 500 recent emails** per address
- **Statistics API** for analytics
- **Zero cost** - completely free with generous rate limits

## 📦 Installation

No external dependencies required! All examples use only Python standard library.

```bash
git clone https://github.com/cleantempmail/cleantempmail-python-examples.git
cd cleantempmail-python-examples
```

For async examples (optional):
```bash
pip install -r requirements.txt
```

## 🔑 API Key

Get your free API key at [CleanTempMail API](https://cleantempmail.com/api)

For testing, use: `ct-test`

## 📚 Examples

### Basic Examples

| File | Description |
|------|-------------|
| [`01_generate_email.py`](01_generate_email.py) | Generate a random temporary email |
| [`02_custom_email.py`](02_custom_email.py) | Create email with custom prefix |
| [`03_receive_email.py`](03_receive_email.py) | Receive and read incoming emails |
| [`04_auto_polling.py`](04_auto_polling.py) | Auto-poll for new emails |
| [`05_delete_email.py`](05_delete_email.py) | Delete specific email |
| [`06_clear_inbox.py`](06_clear_inbox.py) | Clear entire inbox |

### Advanced Examples

| File | Description |
|------|-------------|
| [`07_statistics.py`](07_statistics.py) | Get system statistics |
| [`08_async_client.py`](08_async_client.py) | Async/await API client |
| [`09_verification_code.py`](09_verification_code.py) | Extract verification codes |
| [`10_multiple_addresses.py`](10_multiple_addresses.py) | Manage multiple emails |

### Utility Class

| File | Description |
|------|-------------|
| [`cleantempmail.py`](cleantempmail.py) | Reusable Python client class |
| [`example_client.py`](example_client.py) | How to use the client class |

## 🎯 Quick Start

```python
import requests

# Configuration
API_KEY = "ct-test"
BASE_URL = "https://cleantempmail.com/api"

# Generate email
response = requests.get(
    f"{BASE_URL}/generate-email",
    headers={"X-API-Key": API_KEY}
)
email = response.json()["data"]["email"]
print(f"✅ Generated: {email}")

# Wait for emails
import time
time.sleep(10)

# Get emails
response = requests.get(
    f"{BASE_URL}/emails",
    params={"email": email},
    headers={"X-API-Key": API_KEY}
)
emails = response.json()["data"]["emails"]
print(f"📧 Received {len(emails)} emails")
```

## 📖 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/generate-email` | GET/POST | Generate temporary email |
| `/api/emails` | GET | Get emails for address |
| `/api/email/{id}` | GET | Get single email |
| `/api/email/{id}` | DELETE | Delete email |
| `/api/emails/clear` | DELETE | Clear all emails |
| `/api/stats` | GET | System statistics |
| `/api/statistics/24h` | GET | 24h distribution |
| `/api/statistics/top-subjects` | GET | Popular subjects |
| `/api/statistics/top-domains` | GET | Popular domains |
| `/api/statistics/top-senders` | GET | Popular senders |

## 🔧 Use Cases

- **Testing** - Test email verification flows
- **Automation** - Automate sign-up processes
- **Privacy** - Protect your real email
- **Development** - Test email features without SMTP
- **QA** - Verify email delivery

## 📝 License

MIT License - feel free to use in your projects!

## 🌐 Links

- 🌍 Website: [cleantempmail.com](https://cleantempmail.com)
- 📚 API Docs: [cleantempmail.com/api](https://cleantempmail.com/api)
- 💬 Issues: [GitHub Issues](https://github.com/cleantempmail/cleantempmail-python-examples/issues)

## ⭐ Star Us!

If you find this useful, please star the repository!

---

Made with ❤️ by [CleanTempMail](https://cleantempmail.com)
