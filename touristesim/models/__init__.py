"""
Data Models for TouristeSIM SDK
"""
from typing import Any, Dict, List, Optional


class Model:
    """Base Model class with type casting support"""
    
    casts: Dict[str, str] = {}
    
    def __init__(self, attributes: Optional[Dict[str, Any]] = None):
        self.attributes = {}
        if attributes:
            self.fill(attributes)
    
    def fill(self, attributes: Dict[str, Any]):
        """Fill model with attributes"""
        for key, value in attributes.items():
            self.set_attribute(key, value)
        return self
    
    def set_attribute(self, key: str, value: Any):
        """Set an attribute with type casting if needed"""
        if key in self.casts:
            self.attributes[key] = self._cast(value, self.casts[key])
        else:
            self.attributes[key] = value
    
    def get_attribute(self, key: str) -> Any:
        """Get an attribute"""
        return self.attributes.get(key)
    
    @staticmethod
    def _cast(value: Any, cast_type: str) -> Any:
        """Cast value to specified type"""
        if value is None:
            return value
        
        if cast_type in ('int', 'integer'):
            return int(value)
        elif cast_type in ('float', 'double'):
            return float(value)
        elif cast_type in ('bool', 'boolean'):
            return value in (True, 'true', 1, '1')
        elif cast_type == 'string':
            return str(value)
        elif cast_type == 'array':
            return value if isinstance(value, list) else []
        elif cast_type == 'object':
            return value if isinstance(value, dict) else {}
        
        return value
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get attribute with default"""
        return self.attributes.get(key, default)
    
    def __getitem__(self, key: str) -> Any:
        return self.get(key)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return self.attributes.copy()
    
    def to_json(self) -> str:
        """Convert to JSON"""
        import json
        return json.dumps(self.attributes)


class Plan(Model):
    """Plan Model"""
    
    casts = {
        'id': 'integer',
        'price': 'float',
        'data': 'integer',
        'validity_days': 'integer',
        'reloadable': 'boolean',
        'countries_count': 'integer',
    }
    
    def get_type(self) -> str:
        return self.get('type', 'local')
    
    def is_local(self) -> bool:
        return self.get_type() == 'local'
    
    def is_regional(self) -> bool:
        return self.get_type() == 'regional'
    
    def is_global(self) -> bool:
        return self.get_type() == 'global'
    
    def get_price(self) -> float:
        return self.get('price', 0)
    
    def get_validity_days(self) -> int:
        return self.get('validity_days', 0)
    
    def is_reloadable(self) -> bool:
        return self.get('reloadable', False)
    
    def get_data_gb(self) -> int:
        return int(self.get('data', 0) / 1024)
    
    def is_unlimited(self) -> bool:
        return self.get('data', 0) == 0
    
    def get_countries(self) -> List[str]:
        return self.get('countries', [])
    
    def get_countries_count(self) -> int:
        return self.get('countries_count', 0)
    
    def get_region(self) -> Optional[str]:
        return self.get('region')


class Country(Model):
    """Country Model"""
    
    casts = {
        'plans_count': 'integer',
        'is_featured': 'boolean',
    }
    
    def get_code(self) -> str:
        return self.get('code', '')
    
    def get_name(self) -> str:
        return self.get('name', '')
    
    def get_plans_count(self) -> int:
        return self.get('plans_count', 0)
    
    def is_featured(self) -> bool:
        return self.get('is_featured', False)
    
    def get_flag_url(self) -> str:
        return self.get('flag', '')


class Order(Model):
    """Order Model"""
    
    casts = {
        'id': 'integer',
        'plan_id': 'integer',
        'quantity': 'integer',
        'total_price': 'float',
    }
    
    def get_status(self) -> str:
        return self.get('status', 'pending')
    
    def is_completed(self) -> bool:
        return self.get_status() == 'completed'
    
    def is_pending(self) -> bool:
        return self.get_status() == 'pending'
    
    def is_failed(self) -> bool:
        return self.get_status() == 'failed'
    
    def is_cancelled(self) -> bool:
        return self.get_status() == 'cancelled'
    
    def get_total_price(self) -> float:
        return self.get('total_price', 0)
    
    def get_quantity(self) -> int:
        return self.get('quantity', 0)


class Esim(Model):
    """eSIM Model"""
    
    casts = {
        'balance_data': 'integer',
    }
    
    def get_status(self) -> str:
        return self.get('status', 'pending')
    
    def is_active(self) -> bool:
        return self.get_status() == 'active'
    
    def is_pending(self) -> bool:
        return self.get_status() == 'pending'
    
    def is_expired(self) -> bool:
        return self.get_status() == 'expired'
    
    def is_suspended(self) -> bool:
        return self.get_status() == 'suspended'
    
    def get_iccid(self) -> str:
        return self.get('iccid', '')
    
    def get_balance_data(self) -> int:
        return self.get('balance_data', 0)
    
    def get_validity_end(self) -> Optional[str]:
        return self.get('validity_end')
