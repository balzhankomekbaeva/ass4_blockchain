import requests
import json
import logging

class OllamaService:
    def __init__(self, base_url="http://localhost:11434"):
        """
        Initialize the Ollama service.
        
        Args:
            base_url (str): The base URL of the Ollama API (default: http://localhost:11434)
        """
        self.base_url = base_url
        self.api_url = f"{base_url}/api/generate"
        self.model = "llama3" # You can change this to any model you have installed
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def generate_response(self, user_query):
        """
        Generate a response based on the user's cryptocurrency query.
        
        Args:
            user_query (str): The user's question about cryptocurrency
            
        Returns:
            str: The generated response
        """
        try:
            # Create a system prompt to guide the model's behavior
            system_prompt = """You are a helpful cryptocurrency assistant. 
            Provide accurate information about cryptocurrency prices, market data, and news. 
            Be concise and informative. If you don't know something, say so clearly.
            Focus on facts and avoid speculation."""
            
            # Format the prompt for Ollama
            prompt = f"{system_prompt}\n\nUser: {user_query}\nAssistant:"
            
            # Make the API request to Ollama
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
            
            self.logger.info(f"Sending request to Ollama API with query: {user_query}")
            response = requests.post(self.api_url, json=payload)
            
            if response.status_code != 200:
                self.logger.error(f"Ollama API error: {response.status_code} - {response.text}")
                return "Sorry, I couldn't process your request at the moment. Please try again later."
            
            # Extract the generated text from response
            result = response.json()
            generated_text = result.get("response", "No response received")
            
            self.logger.info(f"Generated response: {generated_text[:100]}...")
            return generated_text
            
        except Exception as e:
            self.logger.error(f"Error in generate_response: {str(e)}")
            return f"Sorry, an error occurred while processing your request: {str(e)}"
    
    def check_availability(self):
        """
        Check if the Ollama API is available.
        
        Returns:
            bool: True if the API is available, False otherwise
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            return response.status_code == 200
        except Exception:
            return False