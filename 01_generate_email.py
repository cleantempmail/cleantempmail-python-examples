#!/usr/bin/env python3
"""
Example 1: Generate a Random Temporary Email

This example shows how to generate a random temporary email address
using the CleanTempMail API.
"""

import json
import urllib.request

# Configuration
API_KEY = "ct-test"
BASE_URL = "https://cleantempmail.com/api"


def generate_random_email():
    """Generate a random temporary email address."""
    
    # Prepare the request
    url = f"{BASE_URL}/generate-email"
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    
    # Make the request
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            
            if data.get("success"):
                email = data["data"]["email"]
                print(f"✅ Successfully generated email: {email}")
                print(f"📬 You can now use this email for registrations")
                print(f"🔗 Direct inbox link: https://cleantempmail.com/{email}")
                return email
            else:
                print(f"❌ Error: {data.get('error', 'Unknown error')}")
                return None
                
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP Error: {e.code} - {e.reason}")
        return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None


if __name__ == "__main__":
    print("=" * 60)
    print("CleanTempMail API - Example 1: Generate Random Email")
    print("=" * 60)
    print()
    
    email = generate_random_email()
    
    if email:
        print()
        print("💡 Tips:")
        print("- The email is active immediately")
        print("- Check emails at /api/emails?email=YOUR_EMAIL")
        print("- Emails are kept for the configured retention period")
