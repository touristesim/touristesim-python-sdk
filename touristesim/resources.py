"""
TouristeSIM SDK Resources
"""
from typing import Dict, Any, List, Optional

from .models import Plan, Country, Order, Esim
from .collections import Collection, PaginatedCollection
from .http_client import HttpClient


class Resource:
    """Base Resource class"""
    
    def __init__(self, client: HttpClient):
        self.client = client


class Plans(Resource):
    """Plans Resource"""
    
    def get(self, filters: Optional[Dict[str, Any]] = None) -> PaginatedCollection:
        """Get all plans with filters"""
        response = self.client.get('/plans', params=filters)
        return PaginatedCollection(
            Collection.make(response.get('data', {}).get('plans', []), Plan).all(),
            response.get('data', {}).get('pagination', {})
        )
    
    def find(self, plan_id: int) -> Plan:
        """Get single plan"""
        response = self.client.get(f'/plans/{plan_id}')
        return Plan(response.get('data', {}))
    
    def validate(self, plan_id: int, quantity: int) -> Dict[str, Any]:
        """Validate plan"""
        response = self.client.post('/plans/validate', {'plan_id': plan_id, 'quantity': quantity})
        return response.get('data', {})
    
    def by_country(self, code: str, per_page: int = 50) -> Collection:
        """Get plans by country"""
        response = self.client.get('/plans', {'country': code, 'per_page': per_page})
        return Collection.make(response.get('data', {}).get('plans', []), Plan)
    
    def by_region(self, slug: str, per_page: int = 50) -> Collection:
        """Get plans by region"""
        response = self.client.get('/plans', {'region': slug, 'per_page': per_page})
        return Collection.make(response.get('data', {}).get('plans', []), Plan)
    
    def global_plans(self, per_page: int = 50) -> Collection:
        """Get global plans"""
        response = self.client.get('/plans', {'type': 'global', 'per_page': per_page})
        return Collection.make(response.get('data', {}).get('plans', []), Plan)


class Countries(Resource):
    """Countries Resource"""
    
    def all(self, filters: Optional[Dict[str, Any]] = None) -> Collection:
        """Get all countries"""
        response = self.client.get('/countries', params=filters)
        return Collection.make(response.get('data', {}).get('countries', []), Country)
    
    def find(self, code: str) -> Optional[Country]:
        """Find country by code"""
        try:
            response = self.client.get(f'/countries/{code}')
            return Country(response.get('data', {}))
        except:
            return None
    
    def search(self, query: str) -> Collection:
        """Search countries"""
        response = self.client.get('/countries', {'search': query})
        return Collection.make(response.get('data', {}).get('countries', []), Country)
    
    def by_region(self, slug: str) -> Collection:
        """Get countries by region"""
        response = self.client.get('/countries', {'region': slug})
        return Collection.make(response.get('data', {}).get('countries', []), Country)
    
    def featured(self) -> Collection:
        """Get featured countries"""
        response = self.client.get('/countries', {'featured': True})
        return Collection.make(response.get('data', {}).get('countries', []), Country)


class Regions(Resource):
    """Regions Resource"""
    
    def all(self) -> List[Dict[str, Any]]:
        """Get all regions"""
        response = self.client.get('/regions')
        return response.get('data', {}).get('regions', [])


class Orders(Resource):
    """Orders Resource"""
    
    def all(self, filters: Optional[Dict[str, Any]] = None) -> PaginatedCollection:
        """Get all orders"""
        response = self.client.get('/orders', params=filters)
        return PaginatedCollection(
            Collection.make(response.get('data', {}).get('orders', []), Order).all(),
            response.get('data', {}).get('pagination', {})
        )
    
    def find(self, order_id: int) -> Order:
        """Get single order"""
        response = self.client.get(f'/orders/{order_id}')
        return Order(response.get('data', {}))
    
    def create(self, data: Dict[str, Any]) -> Order:
        """Create order"""
        response = self.client.post('/orders', data)
        return Order(response.get('data', {}))
    
    def cancel(self, order_id: int) -> bool:
        """Cancel order"""
        self.client.post(f'/orders/{order_id}/cancel', {})
        return True


class Esims(Resource):
    """Esims Resource"""
    
    def all(self, filters: Optional[Dict[str, Any]] = None) -> PaginatedCollection:
        """Get all esims"""
        response = self.client.get('/esims', params=filters)
        return PaginatedCollection(
            Collection.make(response.get('data', {}).get('esims', []), Esim).all(),
            response.get('data', {}).get('pagination', {})
        )
    
    def find(self, iccid: str) -> Esim:
        """Get single esim"""
        response = self.client.get(f'/esims/{iccid}')
        return Esim(response.get('data', {}))
    
    def usage(self, iccid: str) -> Dict[str, Any]:
        """Get esim usage"""
        response = self.client.get(f'/esims/{iccid}/usage')
        return response.get('data', {})
    
    def topup_packages(self, iccid: str) -> Collection:
        """Get topup packages"""
        response = self.client.get(f'/esims/{iccid}/topups')
        return Collection.make(response.get('data', {}).get('packages', []))
    
    def topup(self, iccid: str, package_id: int) -> Dict[str, Any]:
        """Purchase topup"""
        response = self.client.post(f'/esims/{iccid}/topup', {'package_id': package_id})
        return response.get('data', {})
    
    def instructions(self, iccid: str) -> str:
        """Get setup instructions"""
        response = self.client.get(f'/esims/{iccid}/instructions')
        return response.get('data', {}).get('instructions', '')
    
    def send_email(self, iccid: str, email: str) -> bool:
        """Send setup email"""
        self.client.post(f'/esims/{iccid}/send-email', {'email': email})
        return True


class Balance(Resource):
    """Balance Resource"""
    
    def get(self) -> Dict[str, Any]:
        """Get balance"""
        response = self.client.get('/balance')
        return response.get('data', {})
    
    def history(self, filters: Optional[Dict[str, Any]] = None) -> PaginatedCollection:
        """Get balance history"""
        response = self.client.get('/balance/history', params=filters)
        return PaginatedCollection(
            response.get('data', {}).get('history', []),
            response.get('data', {}).get('pagination', {})
        )


class Webhooks(Resource):
    """Webhooks Resource"""
    
    def all(self, filters: Optional[Dict[str, Any]] = None) -> Collection:
        """Get all webhooks"""
        response = self.client.get('/webhooks', params=filters)
        return Collection.make(response.get('data', {}).get('webhooks', []))
    
    def find(self, webhook_id: int) -> Dict[str, Any]:
        """Get single webhook"""
        response = self.client.get(f'/webhooks/{webhook_id}')
        return response.get('data', {})
    
    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create webhook"""
        response = self.client.post('/webhooks', data)
        return response.get('data', {})
    
    def update(self, webhook_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update webhook"""
        response = self.client.put(f'/webhooks/{webhook_id}', data)
        return response.get('data', {})
    
    def delete(self, webhook_id: int) -> bool:
        """Delete webhook"""
        self.client.delete(f'/webhooks/{webhook_id}', {})
        return True
    
    def test(self, webhook_id: int) -> Dict[str, Any]:
        """Test webhook"""
        response = self.client.post(f'/webhooks/{webhook_id}/test', {})
        return response.get('data', {})
