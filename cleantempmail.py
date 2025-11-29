#!/usr/bin/env python3
"""
CleanTempMail API Client

A reusable Python class for interacting with the CleanTempMail API.
This module provides a clean, object-oriented interface to all API endpoints.
"""

import json
import urllib.request
import urllib.parse
from typing import List, Dict, Optional
from datetime import datetime


class CleanTempMailClient:
    """Client for CleanTempMail API."""
    
    def __init__(self, api_key: str, base_url: str = "https://cleantempmail.com/api"):
        """
        Initialize the CleanTempMail client.
        
        Args:
            api_key: Your API key
            base_url: Base URL for the API (default: https://cleantempmail.com/api)
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
    
    def _make_request(self, endpoint: str, method: str = 'GET', data: Optional[Dict] = None) -> Dict:
        """
        Make an HTTP request to the API.
        
        Args:
            endpoint: API endpoint (e.g., '/generate-email')
            method: HTTP method (GET, POST, DELETE)
            data: Request data for POST requests
        
        Returns:
            dict: API response
        
        Raises:
            Exception: If request fails
        """
        url = f"{self.base_url}{endpoint}"
        headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }
        
        # Prepare request
        if data and method == 'POST':
            json_data = json.dumps(data).encode('utf-8')
            req = urllib.request.Request(url, data=json_data, headers=headers, method=method)
        else:
            req = urllib.request.Request(url, headers=headers, method=method)
        
        # Make request
        try:
            with urllib.request.urlopen(req) as response:
                return json.loads(response.read().decode())
        except urllib.error.HTTPError as e:
            error_msg = f"HTTP {e.code}: {e.reason}"
            if e.code == 401:
                error_msg += " (Invalid API key)"
            elif e.code == 429:
                error_msg += " (Rate limit exceeded)"
            raise Exception(error_msg)
    
    def generate_email(self, prefix: Optional[str] = None, domain: Optional[str] = None) -> str:
        """
        Generate a temporary email address.
        
        Args:
            prefix: Custom prefix (optional)
            domain: Specific domain (optional)
        
        Returns:
            str: Generated email address
        """
        data = {}
        if prefix:
            data['prefix'] = prefix
        if domain:
            data['domain'] = domain
        
        if data:
            response = self._make_request('/generate-email', method='POST', data=data)
        else:
            response = self._make_request('/generate-email')
        
        if response.get('success'):
            return response['data']['email']
        else:
            raise Exception(response.get('error', 'Failed to generate email'))
    
    def get_emails(self, email_address: str) -> List[Dict]:
        """
        Get emails for a specific address.
        
        Args:
            email_address: The temporary email address
        
        Returns:
            list: List of email objects
        """
        params = urllib.parse.urlencode({'email': email_address})
        response = self._make_request(f'/emails?{params}')
        
        if response.get('success'):
            return response['data']['emails']
        else:
            raise Exception(response.get('error', 'Failed to get emails'))
    
    def get_email(self, email_id: str) -> Dict:
        """
        Get a single email by ID.
        
        Args:
            email_id: Email ID
        
        Returns:
            dict: Email object
        """
        response = self._make_request(f'/email/{email_id}')
        
        if response.get('success'):
            return response['data']
        else:
            raise Exception(response.get('error', 'Failed to get email'))
    
    def delete_email(self, email_id: str) -> bool:
        """
        Delete a single email.
        
        Args:
            email_id: Email ID
        
        Returns:
            bool: True if deleted successfully
        """
        response = self._make_request(f'/email/{email_id}', method='DELETE')
        return response.get('success', False)
    
    def clear_inbox(self, email_address: str) -> int:
        """
        Clear all emails for an address.
        
        Args:
            email_address: The temporary email address
        
        Returns:
            int: Number of emails deleted
        """
        params = urllib.parse.urlencode({'email': email_address})
        response = self._make_request(f'/emails/clear?{params}', method='DELETE')
        
        if response.get('success'):
            return response['data'].get('count', 0)
        else:
            raise Exception(response.get('error', 'Failed to clear inbox'))
    
    def get_statistics(self) -> Dict:
        """
        Get system statistics.
        
        Returns:
            dict: Statistics object
        """
        response = self._make_request('/stats')
        
        if response.get('success'):
            return response['data']
        else:
            raise Exception(response.get('error', 'Failed to get statistics'))
    
    def get_24h_distribution(self) -> List[Dict]:
        """
        Get 24-hour email distribution.
        
        Returns:
            list: Hourly distribution data
        """
        response = self._make_request('/statistics/24h')
        
        if response.get('success'):
            return response['data']
        else:
            raise Exception(response.get('error', 'Failed to get distribution'))
    
    def get_top_subjects(self, limit: int = 10) -> List[Dict]:
        """
        Get most common email subjects.
        
        Args:
            limit: Number of results (default: 10)
        
        Returns:
            list: Top subjects
        """
        response = self._make_request('/statistics/top-subjects')
        
        if response.get('success'):
            return response['data'][:limit]
        else:
            raise Exception(response.get('error', 'Failed to get top subjects'))
    
    def wait_for_email(self, email_address: str, timeout: int = 60, interval: int = 5) -> Optional[Dict]:
        """
        Wait for a new email to arrive.
        
        Args:
            email_address: Email address to monitor
            timeout: Maximum wait time in seconds
            interval: Polling interval in seconds
        
        Returns:
            dict: First new email or None if timeout
        """
        import time
        
        # Get current email IDs
        initial_emails = self.get_emails(email_address)
        initial_ids = {e['id'] for e in initial_emails}
        
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            time.sleep(interval)
            
            current_emails = self.get_emails(email_address)
            
            # Check for new emails
            for email in current_emails:
                if email['id'] not in initial_ids:
                    return email
        
        return None


if __name__ == "__main__":
    # Quick test
    client = CleanTempMailClient("ct-test")
    
    print("Testing CleanTempMail API Client...")
    print()
    
    # Generate email
    email = client.generate_email()
    print(f"✅ Generated: {email}")
    
    # Get statistics
    stats = client.get_statistics()
    print(f"✅ Total emails in system: {stats.get('total_emails', 0)}")
    
    print("\n💡 Client is ready to use!")
