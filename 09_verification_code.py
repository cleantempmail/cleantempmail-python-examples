"""Extract candidate codes locally without loading remote HTML resources."""
import argparse
import re
from html.parser import HTMLParser
from cleantempmail import CleanTempMailClient
from example_helpers import run


class _TextOnly(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.hidden = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.hidden += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self.hidden:
            self.hidden -= 1
        if tag in ("p", "div", "br", "td"):
            self.parts.append(" ")

    def handle_data(self, data):
        if not self.hidden:
            self.parts.append(data)


def extract_codes(text):
    patterns = [
        r"(?:verification|security|one[- ]time|login)?\s*code\s*(?:is|:|=)?\s*([A-Z0-9-]{4,10})\b",
        r"(?<![0-9])([0-9]{6})(?![0-9])",
        r"(?<![0-9])([0-9]{4})(?![0-9])",
    ]
    codes = []
    for pattern in patterns:
        for code in re.findall(pattern, text, re.IGNORECASE):
            if not any(char.isdigit() for char in code):
                continue
            if code not in codes:
                codes.append(code)
    return codes


def find_verification_codes(email_address, keyword=None):
    client = CleanTempMailClient.from_env()
    results = {}
    # Full inbox response: avoid a second charged request per message.
    for message in client.get_emails(email_address):
        if keyword and keyword.casefold() not in message["subject"].casefold():
            continue
        parser = _TextOnly()
        parser.feed(message.get("html_content", ""))
        text = " ".join((message["subject"], message.get("content", ""), " ".join(parser.parts)))
        codes = extract_codes(text)
        if codes:
            results[message["id"]] = {"subject": message["subject"], "from": message["from_address"], "codes": codes}
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("email")
    parser.add_argument("--keyword", help="Filter by subject")
    args = parser.parse_args()
    results = find_verification_codes(args.email, args.keyword)
    for message_id, result in results.items():
        print(message_id, result["subject"], ", ".join(result["codes"]))
    if not results:
        print("No candidate codes found. Extraction is heuristic; verify against your test email format.")


if __name__ == "__main__":
    run(main)
