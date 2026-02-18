"""
Collection classes for TouristeSIM SDK
"""
from typing import List, Dict, Any, Optional, Callable, TypeVar

T = TypeVar('T')


class Collection:
    """Collection class for handling lists of items"""
    
    def __init__(self, items: List[Any] = None):
        self.items = items or []
    
    @staticmethod
    def make(items: List[Any], model_class: Optional[type] = None):
        """Create collection from raw data with optional model instantiation"""
        if model_class:
            instantiated = []
            for item in items:
                if isinstance(item, model_class):
                    instantiated.append(item)
                else:
                    instantiated.append(model_class(item))
            return Collection(instantiated)
        return Collection(items)
    
    def all(self) -> List[Any]:
        """Get all items"""
        return self.items
    
    def get(self, index: int) -> Optional[Any]:
        """Get item by index"""
        try:
            return self.items[index]
        except IndexError:
            return None
    
    def first(self) -> Optional[Any]:
        """Get first item"""
        return self.items[0] if self.items else None
    
    def last(self) -> Optional[Any]:
        """Get last item"""
        return self.items[-1] if self.items else None
    
    def filter(self, callback: Callable) -> 'Collection':
        """Filter items with callback"""
        filtered = [item for item in self.items if callback(item)]
        return Collection(filtered)
    
    def map(self, callback: Callable) -> 'Collection':
        """Map items with callback"""
        mapped = [callback(item) for item in self.items]
        return Collection(mapped)
    
    def pluck(self, key: str) -> List[Any]:
        """Extract single attribute from all items"""
        return [item.get(key) if hasattr(item, 'get') else item[key] for item in self.items]
    
    def sort(self, callback: Callable) -> 'Collection':
        """Sort items with callback"""
        sorted_items = sorted(self.items, key=callback)
        return Collection(sorted_items)
    
    def sort_by(self, key: str, descending: bool = False) -> 'Collection':
        """Sort items by attribute"""
        def get_value(item):
            return item.get(key) if hasattr(item, 'get') else item[key]
        
        sorted_items = sorted(
            self.items,
            key=get_value,
            reverse=descending
        )
        return Collection(sorted_items)
    
    def push(self, item: Any) -> 'Collection':
        """Add item to collection"""
        self.items.append(item)
        return self
    
    def count(self) -> int:
        """Get item count"""
        return len(self.items)
    
    def is_empty(self) -> bool:
        """Check if collection is empty"""
        return len(self.items) == 0
    
    def to_list(self) -> List[Any]:
        """Convert to list"""
        return self.items.copy()
    
    def to_dict_list(self) -> List[Dict[str, Any]]:
        """Convert items to dictionaries"""
        result = []
        for item in self.items:
            if hasattr(item, 'to_dict'):
                result.append(item.to_dict())
            elif isinstance(item, dict):
                result.append(item)
            else:
                result.append(vars(item))
        return result
    
    def __iter__(self):
        return iter(self.items)
    
    def __len__(self):
        return len(self.items)
    
    def __getitem__(self, index):
        return self.items[index]


class PaginatedCollection(Collection):
    """PaginatedCollection with pagination metadata"""
    
    def __init__(self, items: List[Any] = None, pagination: Optional[Dict[str, Any]] = None):
        super().__init__(items)
        self.pagination = pagination or {}
    
    def get_current_page(self) -> int:
        return self.pagination.get('current_page', 1)
    
    def get_per_page(self) -> int:
        return self.pagination.get('per_page', len(self.items))
    
    def get_total(self) -> int:
        return self.pagination.get('total', len(self.items))
    
    def get_last_page(self) -> int:
        return self.pagination.get('last_page', 1)
    
    def has_more(self) -> bool:
        return self.pagination.get('has_more', self.get_current_page() < self.get_last_page())
    
    def get_pagination(self) -> Dict[str, Any]:
        return self.pagination.copy()
    
    def is_first_page(self) -> bool:
        return self.get_current_page() == 1
    
    def is_last_page(self) -> bool:
        return self.get_current_page() == self.get_last_page()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'data': self.to_dict_list(),
            'pagination': self.pagination,
        }
