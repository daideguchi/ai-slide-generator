"""
Google API Authentication module for Slides and Drive APIs
"""
import os
import pickle
from pathlib import Path
from typing import Optional

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from config.settings import GOOGLE_SLIDES_API_SCOPES, CREDENTIALS_FILE, TOKEN_FILE


class GoogleAPIAuth:
    """Handle Google API authentication and service creation"""
    
    def __init__(self, credentials_file: str = None, token_file: str = None):
        self.credentials_file = credentials_file or CREDENTIALS_FILE
        self.token_file = token_file or TOKEN_FILE
        self.credentials = None
        
    def authenticate(self) -> bool:
        """
        Authenticate with Google API and store credentials
        Returns True if authentication successful
        """
        # Load existing token
        if os.path.exists(self.token_file):
            with open(self.token_file, 'rb') as token:
                self.credentials = pickle.load(token)
        
        # If there are no (valid) credentials available, let the user log in
        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                try:
                    self.credentials.refresh(Request())
                except Exception as e:
                    print(f"Failed to refresh token: {e}")
                    return self._run_auth_flow()
            else:
                return self._run_auth_flow()
        
        # Save the credentials for the next run
        self._save_credentials()
        return True
    
    def _run_auth_flow(self) -> bool:
        """Run the OAuth2 flow to get new credentials"""
        if not os.path.exists(self.credentials_file):
            print(f"Credentials file not found: {self.credentials_file}")
            print("Please download credentials.json from Google Cloud Console")
            return False
        
        try:
            flow = InstalledAppFlow.from_client_secrets_file(
                self.credentials_file, GOOGLE_SLIDES_API_SCOPES
            )
            self.credentials = flow.run_local_server(port=0)
            self._save_credentials()
            return True
        except Exception as e:
            print(f"Authentication failed: {e}")
            return False
    
    def _save_credentials(self):
        """Save credentials to token file"""
        with open(self.token_file, 'wb') as token:
            pickle.dump(self.credentials, token)
    
    def get_slides_service(self):
        """Get Google Slides API service"""
        if not self.credentials:
            raise ValueError("Not authenticated. Call authenticate() first.")
        
        try:
            return build('slides', 'v1', credentials=self.credentials)
        except HttpError as error:
            print(f'An error occurred creating Slides service: {error}')
            raise
    
    def get_drive_service(self):
        """Get Google Drive API service"""
        if not self.credentials:
            raise ValueError("Not authenticated. Call authenticate() first.")
        
        try:
            return build('drive', 'v3', credentials=self.credentials)
        except HttpError as error:
            print(f'An error occurred creating Drive service: {error}')
            raise
    
    def is_authenticated(self) -> bool:
        """Check if currently authenticated"""
        return self.credentials is not None and self.credentials.valid


def setup_google_auth() -> Optional[GoogleAPIAuth]:
    """
    Setup Google authentication
    Returns GoogleAPIAuth instance if successful, None otherwise
    """
    auth = GoogleAPIAuth()
    
    if auth.authenticate():
        print("✓ Google API authentication successful")
        return auth
    else:
        print("✗ Google API authentication failed")
        print("\nTo set up authentication:")
        print("1. Go to Google Cloud Console (https://console.cloud.google.com/)")
        print("2. Create a new project or select existing one")
        print("3. Enable Google Slides API and Google Drive API")
        print("4. Create OAuth 2.0 credentials")
        print("5. Download credentials.json and place in project root")
        return None