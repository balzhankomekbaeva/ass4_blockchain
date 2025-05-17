"""
API client for CryptoPanic
"""

import requests
from typing import Dict, List, Any

class CryptoPanicAPI:
    """Client for interacting with the CryptoPanic API"""
    
    def __init__(self, api_key: str):
        """Initialize with API key"""
        self.api_key = api_key
        self.base_url = "https://cryptopanic.com/api/v1"
    
    def get_news(self, coin_symbol: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Fetch latest news about a specific cryptocurrency from CryptoPanic."""
        url = f"{self.base_url}/posts/"
        params = {
            'auth_token': self.api_key,
            'currencies': coin_symbol,
            'kind': 'news',
            'public': 'true',
            'limit': limit
        }
        
        try:
            response = requests.get(url, params=params)
            data = response.json()
            
            if response.status_code == 200:
                news_items = []
                for item in data.get('results', []):
                    news_items.append({
                        'title': item['title'],
                        'url': item['url'],
                        'source': item['source']['title'],
                        'published_at': item['published_at']
                    })
                return news_items
            else:
                print(f"Error fetching news: {data}")
                return []
        except Exception as e:
            print(f"Error fetching news: {e}")
            return []