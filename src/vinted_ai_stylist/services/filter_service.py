from typing import List, Dict, Optional
from ..models.types import StatusType

class VintedFilterService:
    def __init__(self, items: List[Dict]):
        self.items = items

    def filter_by_brand(self, brand: str) -> List[Dict]:
        """Filter items by brand name (case insensitive)"""
        if not brand:
            return self.items
        return [
            item for item in self.items
            if isinstance(item.get('brand'), str) and item['brand'].lower() == brand.lower()
        ]

    def filter_by_price_range(self, min_price: Optional[float] = None, max_price: Optional[float] = None) -> List[Dict]:
        """Filter items by price range"""
        filtered_items = self.items
        
        if min_price is not None:
            filtered_items = [item for item in filtered_items if float(item['price']) >= float(min_price)]
        
        if max_price is not None:
            filtered_items = [item for item in filtered_items if float(item['price']) <= float(max_price)]
        
        return filtered_items

    def filter_by_size(self, size: str) -> List[Dict]:
        """Filter items by size (case-insensitive, partial match)"""
        if not size:
            return self.items
        return [item for item in self.items if hasattr(item['size'], 'title') and size.lower() in item['size'].title().lower()]

    def filter_by_status(self, status: StatusType) -> List[Dict]:
        """Filter items by status (case insensitive)"""
        if not status:
            return self.items
        return [item for item in self.items if hasattr(item['status'], 'title') and status.lower() == item['status'].title().lower()]

    def filter_by_multiple_criteria(self, brand: Optional[str] = None, 
                                  min_price: Optional[float] = None, 
                                  max_price: Optional[float] = None, 
                                  size: Optional[str] = None, 
                                  status: Optional[StatusType] = None) -> List[Dict]:
        """Filter items by multiple criteria"""
        filtered_items = self.items
        
        if brand:
            filtered_items = self.filter_by_brand(brand)
        
        if min_price is not None or max_price is not None:
            filtered_items = self.filter_by_price_range(min_price, max_price)
        
        if size:
            filtered_items = self.filter_by_size(size)
        
        if status:
            filtered_items = self.filter_by_status(status)
        
        return filtered_items 