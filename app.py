from flask import Flask, render_template, request, jsonify
from api.coinmarketcap import CoinMarketCapAPI
from api.cryptopanic import CryptoPanicAPI
from ai.ollama_service import OllamaService
import os

app = Flask(__name__)

# Load your API keys from environment variables (set them before running)
CMC_API_KEY = os.getenv('CMC_API_KEY')
CRYPTO_PANIC_API_KEY = os.getenv('CRYPTO_PANIC_API_KEY')

# Initialize API clients
cmc_client = CoinMarketCapAPI(CMC_API_KEY)
cryptopanic_client = CryptoPanicAPI(CRYPTO_PANIC_API_KEY)
ollama_service = OllamaService()  # Using default localhost:11434

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/ask', methods=['POST'])
def ask():
    data = request.json
    user_query = data.get('query', '')
    print(f"Received query: {user_query}")
    
    if not user_query:
        return jsonify({'error': 'Query is required'}), 400

    try:
        # Check if Ollama is available
        if not ollama_service.check_availability():
            return jsonify({'error': 'Ollama service is not available. Make sure Ollama is running.'}), 503
            
        response_text = ollama_service.generate_response(user_query)
        print(f"Generated response: {response_text}")
        return jsonify({'response': response_text})
    except Exception as e:
        print(f"Error in /api/ask: {e}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)