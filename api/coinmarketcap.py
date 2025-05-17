"""
API client for CoinMarketCap
"""

import requests
from typing import Dict, List, Any, Optional
    
class CoinMarketCapAPI:
    """Client for interacting with the CoinMarketCap API"""
    
    def __init__(self, api_key: str):
        """Initialize with API key"""
        self.api_key = api_key
        self.base_url = "https://pro-api.coinmarketcap.com/v1"
        self.headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': api_key,
        }
    
    def get_top_coins(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Fetch the top N cryptocurrencies from CoinMarketCap."""
        url = f"{self.base_url}/cryptocurrency/listings/latest"
        parameters = {
            'start': '1',
            'limit': str(limit),
            'convert': 'USD'
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=parameters)
            data = response.json()
            
            if response.status_code == 200:
                coins = []
                for coin in data['data']:
                    coins.append({
                        'id': coin['id'],
                        'name': coin['name'],
                        'symbol': coin['symbol'],
                        'slug': coin['slug'],
                        'rank': coin['cmc_rank'],
                        'market_cap': coin['quote']['USD']['market_cap'],
                        'price': coin['quote']['USD']['price'],
                        'percent_change_24h': coin['quote']['USD']['percent_change_24h']
                    })
                return coins
            else:
                print(f"Error fetching top coins: {data.get('status', {}).get('error_message')}")
                return []
        except Exception as e:
            print(f"Error fetching top coins: {e}")
            return []
    
    def get_coin_details(self, coin_identifier: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific cryptocurrency."""
        # First, need to find the slug or ID of the coin
        url = f"{self.base_url}/cryptocurrency/quotes/latest"
        
        # Try with symbol first
        parameters = {
            'symbol': coin_identifier.upper(),
            'convert': 'USD'
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=parameters)
            data = response.json()
            
            if response.status_code == 200 and len(data.get('data', {})) > 0:
                # Extract the coin data (use the first match if multiple)
                coin_data = next(iter(data['data'].values()))
                
                return {
                    'id': coin_data['id'],
                    'name': coin_data['name'],
                    'symbol': coin_data['symbol'],
                    'slug': coin_data['slug'],
                    'rank': coin_data.get('cmc_rank'),
                    'market_cap': coin_data['quote']['USD']['market_cap'],
                    'price': coin_data['quote']['USD']['price'],
                    'volume_24h': coin_data['quote']['USD']['volume_24h'],
                    'percent_change_24h': coin_data['quote']['USD']['percent_change_24h'],
                    'percent_change_7d': coin_data['quote']['USD']['percent_change_7d'],
                    'max_supply': coin_data.get('max_supply'),
                    'circulating_supply': coin_data.get('circulating_supply'),
                    'total_supply': coin_data.get('total_supply')
                }
            
            # If symbol search fails, try with slug
            parameters = {
                'slug': coin_identifier.lower(),
                'convert': 'USD'
            }
            
            response = requests.get(url, headers=self.headers, params=parameters)
            data = response.json()
            
            if response.status_code == 200 and len(data.get('data', {})) > 0:
                coin_data = next(iter(data['data'].values()))
                
                return {
                    'id': coin_data['id'],
                    'name': coin_data['name'],
                    'symbol': coin_data['symbol'],
                    'slug': coin_data['slug'],
                    'rank': coin_data.get('cmc_rank'),
                    'market_cap': coin_data['quote']['USD']['market_cap'],
                    'price': coin_data['quote']['USD']['price'],
                    'volume_24h': coin_data['quote']['USD']['volume_24h'],
                    'percent_change_24h': coin_data['quote']['USD']['percent_change_24h'],
                    'percent_change_7d': coin_data['quote']['USD']['percent_change_7d'],
                    'max_supply': coin_data.get('max_supply'),
                    'circulating_supply': coin_data.get('circulating_supply'),
                    'total_supply': coin_data.get('total_supply')
                }
            
            print(f"Could not find coin: {coin_identifier}")
            return None
        except Exception as e:
            print(f"Error fetching coin details: {e}")
            return None