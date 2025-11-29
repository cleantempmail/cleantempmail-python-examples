#!/usr/bin/env python3
"""
Example 9: Extract Verification Codes from Emails

This example demonstrates how to extract verification codes
from emails using regular expressions.
"""

import json
import urllib.request
import urllib.parse
import re

# Configuration
API_KEY = "ct-test"
BASE_URL = "https://cleantempmail.com/api"

# Common verification code patterns
PATTERNS = [
    r'\b\d{6}\b',  # 6-digit code
    r'\b\d{4}\b',  # 4-digit code
    r'\b[A-Z0-9]{8}\b',  # 8-character alphanumeric
    r'code[:\s]+([A-Z0-9-]{4,})',  # After "code:"
    r'verification[:\s]+([A-Z0-9-]{4,})',  # After "verification:"
]


def get_emails(email_address):
    """Get all emails for a specific address."""
    params = urllib.parse.urlencode({"email": email_address})
    url = f"{BASE_URL}/emails?{params}"
    headers = {"X-API-Key": API_KEY}
    
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            if data.get("success"):
                return data["data"]["emails"]
    except:
        pass
    return []


def extract_codes(text):
    """
    Extract potential verification codes from text.
    
    Args:
        text (str): Email content
    
    Returns:
        list: List of potential codes
    """
    codes = []
    
    for pattern in PATTERNS:
        matches = re.findall(pattern, text, re.IGNORECASE)
        codes.extend(matches)
    
    # Remove duplicates and filter
    unique_codes = []
    seen = set()
    
    for code in codes:
        code = code.strip()
        if code and code not in seen:
            seen.add(code)
            unique_codes.append(code)
    
    return unique_codes


def find_verification_codes(email_address, keyword=None):
    """
    Find verification codes in emails.
    
    Args:
        email_address (str): Email address to check
        keyword (str, optional): Filter emails by subject keyword
    
    Returns:
        dict: Email ID -> codes mapping
    """
    
    emails = get_emails(email_address)
    
    if not emails:
        return {}
    
    results = {}
    
    for email in emails:
        # Filter by keyword if provided
        if keyword and keyword.lower() not in email['subject'].lower():
            continue
        
        # Extract codes from both subject and content
        text = f"{email['subject']} {email.get('content', '')}"
        codes = extract_codes(text)
        
        if codes:
            results[email['id']] = {
                'subject': email['subject'],
                'from': email['from_address'],
                'codes': codes
            }
    
    return results


if __name__ == "__main__":
    print("=" * 60)
    print("CleanTempMail API - Example 9: Extract Verification Codes")
    print("=" * 60)
    print()
    
    email_address = input("Enter temporary email address: ").strip()
    
    if not email_address:
        print("❌ Email address is required")
        exit(1)
    
    keyword = input("Filter by keyword (optional, press Enter to skip): ").strip()
    
    print(f"\n🔍 Searching for verification codes...")
    
    results = find_verification_codes(email_address, keyword or None)
    
    if not results:
        print("\n📭 No verification codes found")
        print("\n💡 Tips:")
        print("- Make sure you have received emails")
        print("- Try without keyword filter")
        print("- Check if the email contains numeric codes")
    else:
        print(f"\n✅ Found verification codes in {len(results)} email(s)\n")
        
        for email_id, data in results.items():
            print("=" * 60)
            print(f"📧 Email: {data['subject']}")
            print(f"   From: {data['from']}")
            print(f"   Codes found: {', '.join(data['codes'])}")
            print("=" * 60)
            print()
        
        # Show most likely code
        all_codes = []
        for data in results.values():
            all_codes.extend(data['codes'])
        
        if all_codes:
            # Prefer 6-digit codes
            six_digit = [c for c in all_codes if re.match(r'^\d{6}$', c)]
            if six_digit:
                print(f"🎯 Most likely code: {six_digit[0]}")
            else:
                print(f"🎯 First code found: {all_codes[0]}")
        
        print("\n💡 Tips:")
        print("- The most common format is 6-digit numeric codes")
        print("- Codes are extracted using multiple patterns")
        print("- Check the email subject for quick access")
