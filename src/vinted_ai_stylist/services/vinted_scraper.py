import time
import requests
from bs4 import BeautifulSoup
from vinted_scraper.vintedScraper import VintedScraper
from ..models.types import StatusType

class VintedScraperService:
    def __init__(self):
        self.scraper = VintedScraper(
            baseurl="https://www.vinted.co.uk/",
            agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            session_cookie="eyJraWQiOiJFNTdZZHJ1SHBsQWp1MmNObzFEb3JIM2oyN0J1NS1zX09QNVB3UGlobjVNIiwiYWxnIjoiUFMyNTYifQ.eyJhcHBfaWQiOjQsImNsaWVudF9pZCI6IndlYiIsImF1ZCI6ImZyLmNvcmUuYXBpIiwiaXNzIjoidmludGVkLWlhbS1zZXJ2aWNlIiwiaWF0IjoxNzQ1NjA2ODQxLCJzaWQiOiI1ZjBmNzkzZi0xNzQ1NjA2ODQxIiwic2NvcGUiOiJwdWJsaWMiLCJleHAiOjE3NDU2MTQwNDEsInB1cnBvc2UiOiJhY2Nlc3MifQ.fmDfhoRaoT-E1C-uvY6FaLGMYelea3-h8NvmU6ZnaiFbYP5GZrHgr8ESxUvI424W6RrKSq5LK_zcG82ET6tt0tiGze8vbwO8njmse9INQmmdzGxj-BOIS2drpqj4ISnZGe83wxRYWwZkuMuFcZcKf1vOL2w4En0zPv3moKeoifVaXBKzxEW1fa9vpdH2Qh0NuAGxD6potmZN8buX9sBNBnAUXe2PaBAkxZviYLVhgEC5YAtupBd_hXOqmVeK6GogKGh48qNlWBmMtO1Fzz9pj4lFAq6f-wC1uDGZMNw0ZdT0bdyrQpPjmObZnEQj7YpyDkd-p3_Ydzo88pEeAbR-dw",
            ssl_verify=True
        )

    def get_item_description(self, url: str) -> str:
        try:
            time.sleep(0.5)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            description_element = soup.find('span', class_='web_ui__Text__text web_ui__Text__body web_ui__Text__left web_ui__Text__format')
            
            return description_element.get_text(strip=True) if description_element else "Description not found"
        except Exception as e:
            print(f"Error getting description: {str(e)}")
            return "Description not found"

    def get_item_color(self, url: str) -> str:
        try:
            time.sleep(0.5)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            color_element = soup.find('div', class_='details-list__item-value', itemprop='color')
            
            if color_element:
                color_span = color_element.find('span', class_='web_ui__Text__text web_ui__Text__subtitle web_ui__Text__left web_ui__Text__bold')
                return color_span.get_text(strip=True) if color_span else "Color not found"
            return "Color not found"
        except Exception as e:
            print(f"Error getting color: {str(e)}")
            return "Color not found"

    def search_items(self, title: str, brand: str = None, max_price: int = None, 
                    size: str = None, colour: str = None, status: StatusType = None) -> list:
        search_string = f"{colour} {title} {brand} {size} {status}"
        params = {
            "search_text": search_string,
            "page": 1
        }
        
        all_items = []
        item_data_list = []
        
        try:
            items = self.scraper.search(params)
            all_items.extend(items)
            
            for item in all_items:
                item_data = {
                    "id": item.id,
                    "title": item.title,
                    "brand": item.brand.title,
                    "size": item.size,
                    "price": item.price,
                    "url": item.url,
                    "status": item.status,
                    "photos": item.photos
                }
                item_data_list.append(item_data)
            
            return item_data_list
        except Exception as e:
            print(f"An error occurred during search: {str(e)}")
            return [] 