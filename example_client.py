#!/usr/bin/env python3
"""
Example: Using the CleanTempMail Client Class

This example shows how to use the reusable CleanTempMailClient class
for common operations.
"""

from cleantempmail import CleanTempMailClient

# Initialize client
client = CleanTempMailClient("ct-test")


def example_basic_usage():
    """Basic usage example."""
    print("=" * 60)
    print("Example 1: Basic Usage")
    print("=" * 60)
    
    # Generate a random email
    email = client.generate_email()
    print(f"✅ Generated: {email}")
    
    # Get inbox (will be empty initially)
    emails = client.get_emails(email)
    print(f"📬 Inbox has {len(emails)} emails")
    
    print()


def example_custom_email():
    """Custom email generation example."""
    print("=" * 60)
    print("Example 2: Custom Email")
    print("=" * 60)
    
    # Generate with custom prefix
    email = client.generate_email(prefix="mytest")
    print(f"✅ Generated: {email}")
    
    print()


def example_monitoring():
    """Email monitoring example."""
    print("=" * 60)
    print("Example 3: Wait for Email")
    print("=" * 60)
    
    email = client.generate_email()
    print(f"📧 Monitoring: {email}")
    print(f"📤 Send a test email to this address...")
    print(f"⏳ Waiting up to 60 seconds for new email...")
    
    # Wait for email (timeout after 60 seconds)
    new_email = client.wait_for_email(email, timeout=60, interval=5)
    
    if new_email:
        print(f"\n✅ Received email!")
        print(f"   From: {new_email['from_address']}")
        print(f"   Subject: {new_email['subject']}")
    else:
        print(f"\n⏰ No email received within timeout")
    
    print()


def example_statistics():
    """Statistics example."""
    print("=" * 60)
    print("Example 4: Statistics")
    print("=" * 60)
    
    # Get system statistics
    stats = client.get_statistics()
    print(f"📊 System Statistics:")
    print(f"   Total emails: {stats.get('total_emails', 0)}")
    print(f"   Unique subjects: {stats.get('unique_subjects', 0)}")
    print(f"   Active domains: {stats.get('active_domains', 0)}")
    
    # Get top subjects
    top_subjects = client.get_top_subjects(limit=5)
    print(f"\n🏆 Top 5 Subjects:")
    for i, item in enumerate(top_subjects, 1):
        print(f"   {i}. {item['subject']} ({item['count']} emails)")
    
    print()


def example_cleanup():
    """Cleanup example."""
    print("=" * 60)
    print("Example 5: Cleanup")
    print("=" * 60)
    
    email = client.generate_email()
    print(f"📧 Generated: {email}")
    
    # Assume we have some emails
    # In real scenario, you would wait for emails first
    
    # Clear inbox
    count = client.clear_inbox(email)
    print(f"🗑️  Deleted {count} emails from inbox")
    
    print()


if __name__ == "__main__":
    print("=" * 60)
    print("CleanTempMail Client - Usage Examples")
    print("=" * 60)
    print()
    
    try:
        example_basic_usage()
        example_custom_email()
        example_statistics()
        example_cleanup()
        
        # Uncomment to test email monitoring
        # example_monitoring()
        
        print("=" * 60)
        print("✅ All examples completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
