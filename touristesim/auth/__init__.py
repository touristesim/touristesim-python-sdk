"""
OAuth Token classes for TouristeSIM SDK
"""
import time
from datetime import datetime


class Token:
    """OAuth Token class"""
    
    EXPIRATION_BUFFER = 60  # seconds
    
    def __init__(self, data: dict):
        self.access_token = data.get('access_token')
        self.token_type = data.get('token_type', 'Bearer')
        self.expires_in = data.get('expires_in', 3600)
        # Calculate expiration time with buffer
        self.expires_at = int(time.time()) + self.expires_in - self.EXPIRATION_BUFFER
    
    def get_access_token(self) -> str:
        return self.access_token
    
    def get_token_type(self) -> str:
        return self.token_type
    
    def get_expires_in(self) -> int:
        return self.expires_in
    
    def get_expires_at(self) -> int:
        return self.expires_at
    
    def is_expired(self) -> bool:
        return int(time.time()) >= self.expires_at
    
    def get_time_remaining(self) -> int:
        return max(0, self.expires_at - int(time.time()))
    
    def get_authorization_header(self) -> str:
        return f"{self.token_type} {self.access_token}"
    
    def to_dict(self) -> dict:
        return {
            'access_token': self.access_token,
            'token_type': self.token_type,
            'expires_in': self.expires_in,
            'expires_at': self.expires_at,
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(data)


class TokenCache:
    """In-memory token cache"""
    
    def __init__(self, ttl: int = 3600):
        self.ttl = ttl
        self.cache = {}
        self.cache_time = {}
    
    def get(self, key: str) -> Token:
        if key in self.cache:
            # Check if expired
            cache_age = time.time() - self.cache_time.get(key, 0)
            if cache_age < self.ttl:
                token_data = self.cache[key]
                token = Token.from_dict(token_data)
                if not token.is_expired():
                    return token
            # Remove expired cache
            del self.cache[key]
            del self.cache_time[key]
        return None
    
    def store(self, key: str, token: Token):
        self.cache[key] = token.to_dict()
        self.cache_time[key] = time.time()
    
    def forget(self, key: str):
        if key in self.cache:
            del self.cache[key]
            del self.cache_time[key]
    
    def flush(self):
        self.cache.clear()
        self.cache_time.clear()
    
    def has(self, key: str) -> bool:
        return key in self.cache
    
    def clear(self):
        self.cache.clear()
        self.cache_time.clear()
