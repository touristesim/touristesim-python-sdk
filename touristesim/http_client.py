"""
HTTP Client for TouristeSIM SDK
"""
import time
import requests
from typing import Dict, Any, Optional

from .config import Config
from .auth.oauth import OAuthClient
from .exceptions import (
    ApiException,
    AuthenticationException,
    ValidationException,
    RateLimitException,
    ResourceNotFoundException,
    ServerException,
    ConnectionException,
)


class HttpClient:
    """HTTP Client with OAuth, retry logic, and error handling"""
    
    def __init__(self, config: Config, oauth: OAuthClient):
        self.config = config
        self.oauth = oauth
        self.session = requests.Session()
        self.max_retries = config.get_max_retries()
        self.retry_delay_ms = 100
    
    def set_max_retries(self, max_retries: int):
        """Set maximum retry attempts"""
        self.max_retries = max_retries
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make GET request"""
        return self.request('GET', endpoint, params=params)
    
    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make POST request"""
        return self.request('POST', endpoint, data=data)
    
    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make PUT request"""
        return self.request('PUT', endpoint, data=data)
    
    def delete(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make DELETE request"""
        return self.request('DELETE', endpoint, data=data)
    
    def request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make HTTP request with retry logic"""
        last_error = None
        
        for attempt in range(self.max_retries + 1):
            try:
                token = self.oauth.get_token()
                
                headers = {
                    'Authorization': f'Bearer {token}',
                    'User-Agent': self.config.get_user_agent(),
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                }
                
                url = f"{self.config.get_base_url()}{endpoint}"
                
                response = self.session.request(
                    method=method,
                    url=url,
                    params=params,
                    json=data,
                    headers=headers,
                    timeout=self.config.get_timeout(),
                    verify=self.config.should_verify_ssl(),
                )
                
                # Handle errors
                if response.status_code == 401:
                    raise self._map_exception(response)
                
                if response.status_code == 422:
                    raise self._map_exception(response)
                
                if response.status_code == 429:
                    if attempt < self.max_retries:
                        retry_after = int(response.headers.get('Retry-After', 60))
                        time.sleep(retry_after)
                        continue
                    raise self._map_exception(response)
                
                if 400 <= response.status_code < 500:
                    raise self._map_exception(response)
                
                if response.status_code >= 500:
                    if attempt < self.max_retries:
                        time.sleep(self.retry_delay_ms * (attempt + 1) / 1000)
                        continue
                    raise self._map_exception(response)
                
                response.raise_for_status()
                return response.json()
            
            except ConnectionException as e:
                last_error = e
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay_ms * (attempt + 1) / 1000)
                    continue
                raise
            
            except ApiException:
                raise
            
            except requests.exceptions.RequestException as e:
                last_error = e
                if attempt < self.max_retries and self._is_retryable_error(e):
                    time.sleep(self.retry_delay_ms * (attempt + 1) / 1000)
                    continue
                raise self._map_exception_from_request_error(e)
        
        if last_error:
            raise last_error
        
        raise ConnectionException('Request failed after retries')
    
    @staticmethod
    def _is_retryable_error(error: requests.exceptions.RequestException) -> bool:
        """Check if error is retryable"""
        if isinstance(error, requests.exceptions.ConnectTimeout):
            return True
        if isinstance(error, requests.exceptions.ReadTimeout):
            return True
        if isinstance(error, requests.exceptions.ConnectionError):
            return True
        return False
    
    @staticmethod
    def _map_exception(response: requests.Response) -> ApiException:
        """Map HTTP response to exception"""
        status = response.status_code
        try:
            data = response.json()
        except:
            data = {}
        
        message = data.get('message', response.text or 'Unknown error')
        
        if status == 401:
            return AuthenticationException(message, status)
        elif status == 422:
            return ValidationException(message, status, data.get('errors', {}))
        elif status == 429:
            retry_after = int(response.headers.get('Retry-After', 60))
            return RateLimitException(message, retry_after)
        elif status == 404:
            return ResourceNotFoundException(message, status)
        elif status == 503:
            return ServerException(message, status)
        elif status >= 500:
            return ServerException(message, status)
        else:
            return ApiException(message, status, data)
    
    @staticmethod
    def _map_exception_from_request_error(error: requests.exceptions.RequestException) -> ApiException:
        """Map request exception to API exception"""
        if isinstance(error, requests.exceptions.ConnectTimeout):
            return ConnectionException.timeout(str(error))
        elif isinstance(error, requests.exceptions.ReadTimeout):
            return ConnectionException.timeout(str(error))
        elif isinstance(error, requests.exceptions.ConnectionError):
            return ConnectionException.connection_failed(str(error))
        else:
            return ConnectionException(str(error))
