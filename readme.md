# AI Crypto Assistant

AI Crypto Assistant is a Flask-based web application that provides real-time cryptocurrency information, including prices, market data, and news. It integrates data from the CoinMarketCap and CryptoPanic APIs and uses the Ollama service for generating responses.

## Features

* Real-time cryptocurrency prices and market data.
* Latest news and updates about cryptocurrencies.
* Interactive chat interface with popular query suggestions.
* Dynamic response generation using the Ollama AI service.

## Prerequisites

* Python 3.8+
* Flask
* Requests
* Bootstrap (for frontend)
* Ollama service running locally on port 11434
* CoinMarketCap API key
* CryptoPanic API key

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/balzhankomekbaeva/ass4_blockchain.git
   ```

2. Install required packages:

   ```bash
   pip install flask requests
   ```

3. Set environment variables for API keys:

   ```bash
   export CMC_API_KEY='your_coinmarketcap_api_key'
   export CRYPTO_PANIC_API_KEY='your_cryptopanic_api_key'
   ```

4. Run the Ollama service locally:

   ```bash
   ollama serve
   ```

## Running the Application

Start the Flask server:

```bash
python app.py
```

Visit `http://localhost:5000` in your browser to use the AI Crypto Assistant.

## Project Structure

* **app.py**: Main Flask application file.
* **ollama\_service.py**: Handles interaction with the Ollama API.
* **coinmarketcap.py**: Fetches cryptocurrency data from CoinMarketCap.
* **cryptopanic.py**: Retrieves cryptocurrency news from CryptoPanic.
* **templates/index.html**: Frontend interface using Bootstrap.

## Usage

* Enter your query in the chat input (e.g., "Bitcoin price").
* Click on popular queries to get quick answers.
* The assistant will provide real-time data and news.

## Troubleshooting

* Make sure the Ollama service is running before starting the Flask app.
* Check your API keys if you encounter data fetching errors.
* Verify the server is running by accessing `http://localhost:5000`.

## License

MIT License
