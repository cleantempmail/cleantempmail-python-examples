# Quick start

Python 3.10+; no third-party packages required.

```bash
git clone https://github.com/cleantempmail/cleantempmail-python-examples.git
cd cleantempmail-python-examples
export CLEANTEMPMAIL_API_KEY='YOUR_API_KEY'
python3 11_key_usage.py
python3 demo.py
```

Use `python3 demo.py --wait` to monitor the generated address for up to 120 seconds.
Send a test message from your own application after the address is printed.

Without an environment variable, scripts use the shared, limited `ct-test` key.
Buy a production key at [CleanTempMail API](https://cleantempmail.com/api).
Each protected request and every empty inbox poll consumes 1 request; checking
key usage does not. Keys are sent in headers, not URLs.

[Full English guide](README.md) · [完整中文说明](README_CN.md)
