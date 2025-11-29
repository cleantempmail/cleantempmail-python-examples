#!/usr/bin/env python3
"""
CleanTempMail API - Complete Demo

This demo showcases all major features of the CleanTempMail API.
Run this script to see a complete workflow demonstration.
"""

import json
import urllib.request
import urllib.parse
import time
import re
from datetime import datetime

# Configuration
API_KEY = "ct-test"
BASE_URL = "https://cleantempmail.com/api"


class Colors:
    """Terminal colors for better output."""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_header(text):
    """Print a colored header."""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 60}{Colors.END}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text}{Colors.END}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 60}{Colors.END}\n")


def print_success(text):
    """Print success message."""
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")


def print_info(text):
    """Print info message."""
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.END}")


def print_warning(text):
    """Print warning message."""
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")


def api_request(endpoint, method='GET', data=None):
    """Make an API request."""
    url = f"{BASE_URL}{endpoint}"
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    
    if data and method == 'POST':
        json_data = json.dumps(data).encode('utf-8')
        req = urllib.request.Request(url, data=json_data, headers=headers, method=method)
    else:
        req = urllib.request.Request(url, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print_warning(f"Request failed: {str(e)}")
        return None


def demo_generate_email():
    """Demo: Generate temporary email."""
    print_header("Demo 1: Generate Temporary Email")
    
    # Generate random email
    print_info("Generating random email address...")
    response = api_request('/generate-email')
    
    if response and response.get('success'):
        email = response['data']['email']
        print_success(f"Generated: {email}")
        print_info(f"Direct link: https://cleantempmail.com/{email}")
        return email
    else:
        print_warning("Failed to generate email")
        return None


def demo_custom_email():
    """Demo: Generate custom email."""
    print_header("Demo 2: Custom Email Generation")
    
    print_info("Generating email with custom prefix 'demo123'...")
    response = api_request('/generate-email', method='POST', data={"prefix": "demo123"})
    
    if response and response.get('success'):
        email = response['data']['email']
        print_success(f"Generated: {email}")
        return email
    else:
        print_warning("Failed to generate custom email")
        return None


def demo_receive_emails(email_address):
    """Demo: Receive emails."""
    print_header("Demo 3: Check Inbox")
    
    print_info(f"Checking inbox for: {email_address}")
    params = urllib.parse.urlencode({'email': email_address})
    response = api_request(f'/emails?{params}')
    
    if response and response.get('success'):
        emails = response['data']['emails']
        count = len(emails)
        
        if count == 0:
            print_info("Inbox is currently empty")
        else:
            print_success(f"Found {count} email(s)")
            
            # Show first email details
            first_email = emails[0]
            print(f"\n📧 Latest Email:")
            print(f"   From: {first_email['from_address']}")
            print(f"   Subject: {first_email['subject']}")
            timestamp = datetime.fromtimestamp(first_email.get('timestamp', 0))
            print(f"   Time: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
            
        return emails
    else:
        print_warning("Failed to fetch emails")
        return []


def demo_statistics():
    """Demo: Get system statistics."""
    print_header("Demo 4: System Statistics")
    
    print_info("Fetching system statistics...")
    response = api_request('/stats')
    
    if response and response.get('success'):
        stats = response['data']
        print_success("Statistics retrieved:")
        print(f"   📊 Total emails: {stats.get('total_emails', 0)}")
        print(f"   🏷️  Unique subjects: {stats.get('unique_subjects', 0)}")
        print(f"   🌐 Active domains: {stats.get('active_domains', 0)}")
        
        return stats
    else:
        print_warning("Failed to fetch statistics")
        return None


def demo_top_subjects():
    """Demo: Get top subjects."""
    print_header("Demo 5: Popular Email Subjects")
    
    print_info("Fetching top subjects...")
    response = api_request('/statistics/top-subjects')
    
    if response and response.get('success'):
        subjects = response['data'][:5]  # Top 5
        print_success(f"Found {len(subjects)} popular subjects:")
        
        for i, item in enumerate(subjects, 1):
            print(f"   {i}. {item['subject']} ({item['count']} emails)")
        
        return subjects
    else:
        print_warning("Failed to fetch top subjects")
        return []


def demo_verification_code(email_address):
    """Demo: Extract verification codes."""
    print_header("Demo 6: Verification Code Extraction")
    
    print_info("Searching for verification codes...")
    params = urllib.parse.urlencode({'email': email_address})
    response = api_request(f'/emails?{params}')
    
    if response and response.get('success'):
        emails = response['data']['emails']
        
        # Search for codes in emails
        patterns = [r'\b\d{6}\b', r'\b\d{4}\b']
        found_codes = []
        
        for email in emails:
            text = f"{email['subject']} {email.get('content', '')}"
            for pattern in patterns:
                codes = re.findall(pattern, text)
                found_codes.extend(codes)
        
        if found_codes:
            print_success(f"Found {len(found_codes)} potential verification code(s):")
            for code in set(found_codes)[:5]:  # Show unique codes
                print(f"   🔢 {code}")
        else:
            print_info("No verification codes found")
        
        return found_codes
    else:
        print_warning("Failed to search for codes")
        return []


def demo_clear_inbox(email_address):
    """Demo: Clear inbox."""
    print_header("Demo 7: Clear Inbox")
    
    print_info(f"Clearing inbox for: {email_address}")
    params = urllib.parse.urlencode({'email': email_address})
    response = api_request(f'/emails/clear?{params}', method='DELETE')
    
    if response and response.get('success'):
        count = response['data'].get('count', 0)
        print_success(f"Deleted {count} email(s)")
        return count
    else:
        print_info("Inbox already empty or failed to clear")
        return 0


def main():
    """Run the complete demo."""
    print(f"{Colors.BOLD}")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║                                                            ║")
    print("║          CleanTempMail API - Complete Demo                ║")
    print("║                                                            ║")
    print("║  This demo showcases all major API features               ║")
    print("║                                                            ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}\n")
    
    time.sleep(1)
    
    # Demo 1: Generate random email
    email1 = demo_generate_email()
    if not email1:
        print_warning("Demo stopped due to error")
        return
    
    time.sleep(1)
    
    # Demo 2: Generate custom email
    email2 = demo_custom_email()
    
    time.sleep(1)
    
    # Demo 3: Check inbox
    demo_receive_emails(email1)
    
    time.sleep(1)
    
    # Demo 4: System statistics
    demo_statistics()
    
    time.sleep(1)
    
    # Demo 5: Top subjects
    demo_top_subjects()
    
    time.sleep(1)
    
    # Demo 6: Verification codes
    demo_verification_code(email1)
    
    time.sleep(1)
    
    # Demo 7: Clear inbox (optional)
    # Uncomment if you want to test clearing
    # demo_clear_inbox(email1)
    
    # Summary
    print_header("Demo Complete!")
    print_success("All API features demonstrated successfully!")
    print()
    print(f"{Colors.BLUE}📚 Learn more:{Colors.END}")
    print(f"   🌐 Website: https://cleantempmail.com")
    print(f"   📖 API Docs: https://cleantempmail.com/api")
    print(f"   💻 GitHub: https://github.com/cleantempmail/cleantempmail-python-examples")
    print()
    print(f"{Colors.GREEN}💡 Tips:{Colors.END}")
    print(f"   • Use API key 'ct-test' for testing")
    print(f"   • Each address supports up to 500 recent emails")
    print(f"   • Emails are kept for the configured retention period")
    print(f"   • Check individual examples for more details")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⏹️  Demo interrupted by user{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}❌ Error: {str(e)}{Colors.END}")
