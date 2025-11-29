#!/usr/bin/env python3
"""
Example 4: Auto-Polling for New Emails

This example shows how to continuously check for new emails
and display them as they arrive (useful for automation).
"""

import json
import urllib.request
import urllib.parse
import time
from datetime import datetime

# Configuration
API_KEY = "ct-test"
BASE_URL = "https://cleantempmail.com/api"
POLL_INTERVAL = 5  # seconds


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


def auto_poll(email_address, duration_minutes=5):
    """
    Automatically poll for new emails.
    
    Args:
        email_address (str): Email address to monitor
        duration_minutes (int): How long to monitor (minutes)
    """
    
    print(f"🔄 Monitoring: {email_address}")
    print(f"⏱️  Duration: {duration_minutes} minutes")
    print(f"📡 Polling interval: {POLL_INTERVAL} seconds")
    print("\nPress Ctrl+C to stop monitoring\n")
    print("=" * 60)
    
    seen_ids = set()
    start_time = time.time()
    end_time = start_time + (duration_minutes * 60)
    
    try:
        while time.time() < end_time:
            emails = get_emails(email_address)
            
            # Check for new emails
            new_emails = [e for e in emails if e['id'] not in seen_ids]
            
            if new_emails:
                for email in new_emails:
                    seen_ids.add(email['id'])
                    
                    # Display notification
                    timestamp = datetime.fromtimestamp(email.get('timestamp', 0))
                    print(f"\n📧 NEW EMAIL RECEIVED!")
                    print(f"   From: {email['from_address']}")
                    print(f"   Subject: {email['subject']}")
                    print(f"   Time: {timestamp.strftime('%H:%M:%S')}")
                    print("-" * 60)
            else:
                # Show heartbeat
                elapsed = int(time.time() - start_time)
                remaining = int(end_time - time.time())
                print(f"\r⏳ Waiting for emails... (elapsed: {elapsed}s, remaining: {remaining}s)", end="", flush=True)
            
            time.sleep(POLL_INTERVAL)
        
        print(f"\n\n✅ Monitoring completed")
        print(f"📊 Total emails received: {len(seen_ids)}")
        
    except KeyboardInterrupt:
        print(f"\n\n⏹️  Monitoring stopped by user")
        print(f"📊 Total emails received: {len(seen_ids)}")


if __name__ == "__main__":
    print("=" * 60)
    print("CleanTempMail API - Example 4: Auto-Polling")
    print("=" * 60)
    print()
    
    email_address = input("Enter temporary email address to monitor: ").strip()
    
    if not email_address:
        print("❌ Email address is required")
        exit(1)
    
    try:
        duration = int(input("Enter monitoring duration in minutes (default: 5): ") or "5")
    except:
        duration = 5
    
    print()
    auto_poll(email_address, duration)
    
    print("\n💡 Tips:")
    print("- Use this for automated testing workflows")
    print("- Combine with verification code extraction")
    print("- Adjust POLL_INTERVAL based on your needs")
