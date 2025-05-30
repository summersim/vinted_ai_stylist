import unittest
from src.vinted_ai_stylist.services.filter_service import VintedFilterService

class TestVintedFilterService(unittest.TestCase):
    def setUp(self):
        self.test_items = [
            {
                "id": "1",
                "title": "Zara Dress",
                "brand": "Zara",
                "size": "S",
                "price": "25.00",
                "status": "New with tags"
            },
            {
                "id": "2",
                "title": "H&M Shirt",
                "brand": "H&M",
                "size": "M",
                "price": "15.00",
                "status": "Very good"
            }
        ]
        self.filter_service = VintedFilterService(self.test_items)

    def test_filter_by_brand(self):
        filtered_items = self.filter_service.filter_by_brand("Zara")
        self.assertEqual(len(filtered_items), 1)
        self.assertEqual(filtered_items[0]["brand"], "Zara")

    def test_filter_by_price_range(self):
        filtered_items = self.filter_service.filter_by_price_range(min_price=20, max_price=30)
        self.assertEqual(len(filtered_items), 1)
        self.assertEqual(filtered_items[0]["price"], "25.00")

    def test_filter_by_size(self):
        filtered_items = self.filter_service.filter_by_size("S")
        self.assertEqual(len(filtered_items), 1)
        self.assertEqual(filtered_items[0]["size"], "S")

    def test_filter_by_status(self):
        filtered_items = self.filter_service.filter_by_status("New with tags")
        self.assertEqual(len(filtered_items), 1)
        self.assertEqual(filtered_items[0]["status"], "New with tags")

    def test_filter_by_multiple_criteria(self):
        filtered_items = self.filter_service.filter_by_multiple_criteria(
            brand="Zara",
            min_price=20,
            max_price=30,
            size="S",
            status="New with tags"
        )
        self.assertEqual(len(filtered_items), 1)
        self.assertEqual(filtered_items[0]["brand"], "Zara")
        self.assertEqual(filtered_items[0]["price"], "25.00")
        self.assertEqual(filtered_items[0]["size"], "S")
        self.assertEqual(filtered_items[0]["status"], "New with tags")

if __name__ == '__main__':
    unittest.main() 