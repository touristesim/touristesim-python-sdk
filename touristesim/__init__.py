"""
TouristeSIM Python SDK - Main entry point
"""
from typing import Optional, Dict, Any

from .config import Config
from .http_client import HttpClient
from .auth.oauth import OAuthClient
from .resources import (
    Plans,
    Countries,
    Regions,
    Orders,
    Esims,
    Balance,
    Webhooks,
)


class TouristEsim:
    """
    Main Tourist eSIM SDK class
    """
    
    VERSION = '1.0.0'
    
    def __init__(self, client_id: str, client_secret: str, options: Optional[Dict[str, Any]] = None):
        self.config = Config(client_id, client_secret, options)
        self.oauth = OAuthClient(self.config)
        self.http_client = HttpClient(self.config, self.oauth)
        
        # Lazy load resources
        self._plans_resource: Optional[Plans] = None
        self._countries_resource: Optional[Countries] = None
        self._regions_resource: Optional[Regions] = None
        self._orders_resource: Optional[Orders] = None
        self._esims_resource: Optional[Esims] = None
        self._balance_resource: Optional[Balance] = None
        self._webhooks_resource: Optional[Webhooks] = None
    
    def plans(self) -> Plans:
        """Get Plans resource"""
        if self._plans_resource is None:
            self._plans_resource = Plans(self.http_client)
        return self._plans_resource
    
    def countries(self) -> Countries:
        """Get Countries resource"""
        if self._countries_resource is None:
            self._countries_resource = Countries(self.http_client)
        return self._countries_resource
    
    def regions(self) -> Regions:
        """Get Regions resource"""
        if self._regions_resource is None:
            self._regions_resource = Regions(self.http_client)
        return self._regions_resource
    
    def orders(self) -> Orders:
        """Get Orders resource"""
        if self._orders_resource is None:
            self._orders_resource = Orders(self.http_client)
        return self._orders_resource
    
    def esims(self) -> Esims:
        """Get Esims resource"""
        if self._esims_resource is None:
            self._esims_resource = Esims(self.http_client)
        return self._esims_resource
    
    def balance(self) -> Balance:
        """Get Balance resource"""
        if self._balance_resource is None:
            self._balance_resource = Balance(self.http_client)
        return self._balance_resource
    
    def webhooks(self) -> Webhooks:
        """Get Webhooks resource"""
        if self._webhooks_resource is None:
            self._webhooks_resource = Webhooks(self.http_client)
        return self._webhooks_resource
    
    def get_config(self) -> Config:
        """Get config instance"""
        return self.config
    
    def get_http_client(self) -> HttpClient:
        """Get HTTP client instance"""
        return self.http_client
    
    @classmethod
    def version(cls) -> str:
        """Get SDK version"""
        return cls.VERSION


# Export public API
__all__ = [
    'TouristEsim',
    'Config',
]
