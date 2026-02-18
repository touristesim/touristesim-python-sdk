"""
API Exception classes for TouristeSIM SDK
"""


class ApiException(Exception):
    """Base API Exception class"""
    
    def __init__(self, message: str, status_code: int = 0, response: dict = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response = response or {}
        self.request_id = None
    
    def get_status_code(self) -> int:
        return self.status_code
    
    def get_response(self) -> dict:
        return self.response
    
    def get_request_id(self) -> str:
        return self.request_id


class AuthenticationException(ApiException):
    """Authentication Exception - 401 Unauthorized"""
    
    @staticmethod
    def invalid_credentials(message: str = 'Invalid client credentials'):
        return AuthenticationException(message, 401)
    
    @staticmethod
    def token_expired(message: str = 'Token has expired'):
        return AuthenticationException(message, 401)
    
    @staticmethod
    def unauthorized(message: str = 'Unauthorized'):
        return AuthenticationException(message, 401)


class ValidationException(ApiException):
    """Validation Exception - 422 Unprocessable Entity"""
    
    def __init__(self, message: str = 'Validation failed', status_code: int = 422, errors: dict = None):
        super().__init__(message, status_code)
        self.errors = errors or {}
    
    def get_errors(self) -> dict:
        return self.errors
    
    def set_errors(self, errors: dict):
        self.errors = errors


class RateLimitException(ApiException):
    """Rate Limit Exception - 429 Too Many Requests"""
    
    def __init__(self, message: str = 'Rate limit exceeded', retry_after: int = 60):
        super().__init__(message, 429)
        self.retry_after = retry_after
    
    def get_retry_after(self) -> int:
        return self.retry_after
    
    def set_retry_after(self, retry_after: int):
        self.retry_after = retry_after


class ResourceNotFoundException(ApiException):
    """Resource Not Found Exception - 404 Not Found"""
    
    @staticmethod
    def plan(plan_id):
        return ResourceNotFoundException(f'Plan with ID {plan_id} not found', 404)
    
    @staticmethod
    def order(order_id):
        return ResourceNotFoundException(f'Order with ID {order_id} not found', 404)
    
    @staticmethod
    def esim(iccid: str):
        return ResourceNotFoundException(f'eSIM with ICCID {iccid} not found', 404)
    
    def __init__(self, message: str = 'Resource not found', status_code: int = 404):
        super().__init__(message, status_code)


class ServerException(ApiException):
    """Server Exception - 5xx Server Errors"""
    
    @staticmethod
    def maintenance(message: str = 'Server is under maintenance'):
        return ServerException(message, 503)
    
    def __init__(self, message: str = 'Server error', status_code: int = 500):
        super().__init__(message, status_code)


class ConnectionException(ApiException):
    """Connection Exception - Network/Timeout Errors"""
    
    @staticmethod
    def timeout(message: str = 'Request timeout'):
        return ConnectionException(message)
    
    @staticmethod
    def connection_failed(message: str = 'Connection failed'):
        return ConnectionException(message)
    
    def __init__(self, message: str = 'Connection error', status_code: int = 0):
        super().__init__(message, status_code)
