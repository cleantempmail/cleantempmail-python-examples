#!/usr/bin/env python3
"""
Example 3: Receive and Read Emails

This example demonstrates how to check for incoming emails
and display their content.
"""

import json
import urllib.request
import urllib.parse
from datetime import datetime

# Configuration
API_KEY = "ct-test"
BASE_URL = "https://cleantempmail.com/api"


def get_emails(email_address):
    """
    Get all emails for a specific address.
    
    Args:
        email_address (str): The temporary email address
    
    Returns:
        list: List of email objects
    """
    
    # Prepare the request
    params = urllib.parse.urlencode({"email": email_address})
    url = f"{BASE_URL}/emails?{params}"
    headers = {"X-API-Key": API_KEY}
    
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            
            if data.get("success"):
                return data["data"]["emails"]
            else:
                print(f"❌ Error: {data.get('error', 'Unknown error')}")
                return []
                
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return []


def display_email(email):
    """Display email details in a formatted way."""
    
    print("\n" + "=" * 60)
    print(f"📧 Email ID: {email['id']}")
    print("-" * 60)
    print(f"From: {email['from_address']}")
    print(f"To: {email['email_address']}")
    print(f"Subject: {email['subject']}")
    
    # Convert timestamp to readable date
    timestamp = email.get('timestamp', 0)
    date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    print(f"Date: {date}")
    print("-" * 60)
    
    # Display content (truncate if too long)
    content = email.get('content', 'No content')
    if len(content) > 500:
        print(f"Content (truncated):\n{content[:500]}...")
    else:
        print(f"Content:\n{content}")
    
    # HTML content
    if email.get('has_html'):
        print("\n📎 This email contains HTML content")
    
    print("=" * 60)


if __name__ == "__main__":
    print("=" * 60)
    print("CleanTempMail API - Example 3: Receive Emails")
    print("=" * 60)
    print()
    
    # You can use an existing email or generate a new one
    email_address = input("Enter temporary email address: ").strip()
    
    if not email_address:
        print("❌ Email address is required")
        exit(1)
    
    print(f"\n📬 Checking inbox for: {email_address}")
    print("Please wait...")
    
    emails = get_emails(email_address)
    
    if not emails:
        print("\n📭 Inbox is empty")
        print(f"\n💡 Tip: Send an email to {email_address} and run this script again")
    else:
        print(f"\n✅ Found {len(emails)} email(s)\n")
        
        for i, email in enumerate(emails, 1):
            print(f"\n--- Email {i}/{len(emails)} ---")
            display_email(email)
        
        print("\n💡 Tips:")
        print("- Use /api/email/{id} to get full details of a single email")
        print("- Emails are sorted by timestamp (newest first)")
        print("- Maximum 500 recent emails are returned")
