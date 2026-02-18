import os
import json
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

class Config:
    """Configuration class for TouristeSIM Python SDK"""
    
    def __init__(self, client_id: str, client_secret: str, options: Optional[Dict[str, Any]] = None):
        self.client_id = client_id
        self.client_secret = client_secret
        
        options = options or {}
        self.base_url = options.get('base_url', 'https://api.touristesim.net/v1').rstrip('/')
        self.mode = options.get('mode', 'sandbox')
        self.timeout = options.get('timeout', 30)
        self.connect_timeout = options.get('connect_timeout', 10)
        self.verify_ssl = options.get('verify_ssl', True)
        self.user_agent = options.get('user_agent') or self._get_default_user_agent()
        self.max_retries = options.get('max_retries', 3)
    
    def get_client_id(self) -> str:
        return self.client_id
    
    def get_client_secret(self) -> str:
        return self.client_secret
    
    def get_base_url(self) -> str:
        return self.base_url
    
    def get_mode(self) -> str:
        return self.mode
    
    def is_sandbox(self) -> bool:
        return self.mode == 'sandbox'
    
    def is_production(self) -> bool:
        return self.mode == 'production'
    
    def should_verify_ssl(self) -> bool:
        return self.verify_ssl
    
    def get_timeout(self) -> int:
        return self.timeout
    
    def get_connect_timeout(self) -> int:
        return self.connect_timeout
    
    def get_user_agent(self) -> str:
        return self.user_agent
    
    def get_max_retries(self) -> int:
        return self.max_retries
    
    def get_oauth_token_url(self) -> str:
        return f"{self.base_url}/../oauth/token"
    
    def _get_default_user_agent(self) -> str:
        import sys
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        return f"TouristeSIM-SDK/1.0.0 (Python/{python_version})"
    
    def get_http_client_options(self) -> Dict[str, Any]:
        return {
            'base_url': self.base_url,
            'timeout': self.timeout,
            'connect_timeout': self.connect_timeout,
            'verify': self.verify_ssl,
            'headers': {
                'User-Agent': self.get_user_agent(),
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
        }
