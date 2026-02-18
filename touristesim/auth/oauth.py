"""
OAuth Client for TouristeSIM SDK
"""
import requests
from typing import Optional

from .import Token, TokenCache
from ..config import Config
from ..exceptions import AuthenticationException


class OAuthClient:
    """OAuth 2.0 Client for handling authentication"""
    
    def __init__(self, config: Config):
        self.config = config
        self.token: Optional[Token] = None
        self.token_cache = TokenCache()
        self.http_client = requests.Session()
    
    def get_token(self) -> str:
        """Get valid access token"""
        valid_token = self.get_valid_token()
        return valid_token.get_access_token()
    
    def get_valid_token(self) -> Token:
        """Get valid token, refreshing if necessary"""
        # Check if we have a cached token that's still valid
        if self.token and not self.token.is_expired():
            return self.token
        
        # Try to get from file cache
        cached_token = self.token_cache.get('oauth_token')
        if cached_token and not cached_token.is_expired():
            self.token = cached_token
            return self.token
        
        # Request new token
        self.token = self.request_token()
        self.token_cache.store('oauth_token', self.token)
        return self.token
    
    def request_token(self) -> Token:
        """Request new OAuth token"""
        try:
            response = self.http_client.post(
                self.config.get_oauth_token_url(),
                data={
                    'grant_type': 'client_credentials',
                    'client_id': self.config.get_client_id(),
                    'client_secret': self.config.get_client_secret(),
                },
                headers={
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'User-Agent': self.config.get_user_agent(),
                    'Accept': 'application/json',
                },
                timeout=self.config.get_timeout(),
                verify=self.config.should_verify_ssl(),
            )
            
            if response.status_code == 401:
                raise AuthenticationException.invalid_credentials('Invalid client credentials')
            
            response.raise_for_status()
            return Token(response.json())
        
        except requests.exceptions.RequestException as e:
            if hasattr(e.response, 'status_code') and e.response.status_code == 401:
                raise AuthenticationException.invalid_credentials(str(e))
            raise
    
    def revoke_token(self) -> bool:
        """Revoke token and clear cache"""
        self.token = None
        self.token_cache.forget('oauth_token')
        return True
