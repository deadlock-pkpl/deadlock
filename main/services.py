import requests
import urllib.parse
from django.conf import settings

class GoogleOAuthService:
    def __init__(self):
        self.client_id = settings.GOOGLE_CLIENT_ID
        self.client_secret = settings.GOOGLE_CLIENT_SECRET
        self.redirect_uri = settings.GOOGLE_REDIRECT_URI
        self.auth_url = "https://accounts.google.com/o/oauth2/auth"
        self.token_url = "https://oauth2.googleapis.com/token"

    def get_authorization_url(self):
        """Menghasilkan URL untuk dilempar ke browser user"""
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'scope': 'profile email',
            'response_type': 'code',
            'state': 'random_secure_string',
            'access_type': 'offline',
            'prompt': 'select_account'
        }
        return f"{self.auth_url}?{urllib.parse.urlencode(params)}"

    def get_tokens(self, code):
        """Menukar 'code' dari callback menjadi access_token & refresh_token"""
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.redirect_uri,
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        response = requests.post(self.token_url, data=data)
        return response.json() if response.status_code == 200 else None

    def get_user_info(self, access_token):
        """Mengambil data profil user menggunakan token"""
        response = requests.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={'Authorization': f"Bearer {access_token}"}
        )
        return response.json()