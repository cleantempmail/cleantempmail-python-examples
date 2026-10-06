# Contributing

Match the current [API contract](https://cleantempmail.com/api). Keep examples
small and use the Python 3.10+ standard library. Include quota cost and avoid
unbounded polling, silent failures, hardcoded active domains and real credentials.

Run:

```bash
python3 -m unittest discover -s tests -v
python3 -m compileall -q .
```

Tests must use synthetic data and a local mock API; do not require a paid key or
read another user's inbox. Update all six README translations when behavior or
setup instructions change. Create a branch and submit a pull request to this
repository. Do not commit `.env` files, downloaded messages or attachments.
