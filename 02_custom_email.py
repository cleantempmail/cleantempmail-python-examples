#!/usr/bin/env python3
"""
Example 2: Generate Custom Email with Specific Prefix

This example shows how to create a temporary email with your own
custom prefix and optionally choose a specific domain.
"""

import json
import urllib.request
import urllib.parse

# Configuration
API_KEY = "ct-test"
BASE_URL = "https://cleantempmail.com/api"


def generate_custom_email(prefix, domain=None):
    """
    Generate a custom temporary email address.
    
    Args:
        prefix (str): Custom prefix for the email (e.g., "mytest")
        domain (str, optional): Specific domain to use
    
    Returns:
        str: Generated email address or None if failed
    """
    
    # Prepare the request data
    data = {"prefix": prefix}
    if domain:
        data["domain"] = domain
    
    # Prepare the request
    url = f"{BASE_URL}/generate-email"
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(url, data=json_data, headers=headers, method='POST')
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode())
            
            if result.get("success"):
                email = result["data"]["email"]
                print(f"✅ Successfully generated: {email}")
                return email
            else:
                print(f"❌ Error: {result.get('error', 'Unknown error')}")
                return None
                
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP Error: {e.code} - {e.reason}")
        return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None


if __name__ == "__main__":
    print("=" * 60)
    print("CleanTempMail API - Example 2: Custom Email Generation")
    print("=" * 60)
    print()
    
    # Example 1: Custom prefix
    print("📧 Generating email with custom prefix 'testuser'...")
    email1 = generate_custom_email("testuser")
    print()
    
    # Example 2: Custom prefix and domain
    print("📧 Generating email with prefix 'demo' and specific domain...")
    email2 = generate_custom_email("demo", "example.com")
    print()
    
    print("💡 Tips:")
    print("- Prefix must be 3-20 characters")
    print("- Only letters, numbers, dots, hyphens, underscores allowed")
    print("- If domain is not provided, a random one will be chosen")
    print("- If domain is not active, a random one will be used")
