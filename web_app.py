from flask import Flask, request, render_template, send_from_directory
import os
from dotenv import load_dotenv
load_dotenv()

import logging
import sys
from config import config
from data_loader import DataLoader
from embedder import Embedder
from indexer import Indexer
from llm_handler import LLMHandler
from query_engine import QueryEngine

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
logger = logging.getLogger(__name__)

# Add diagnostic logs for UI/UX issues
logger.info("Flask app starting up")

# Initialize Flask app
app = Flask(__name__)

# Initialize components
data_loader = DataLoader()
embedder = Embedder()
indexer = Indexer(embedder=embedder)
llm_handler = LLMHandler()
query_engine = QueryEngine(indexer=indexer, llm_handler=llm_handler, data_loader=data_loader)

# Check if index is ready
index_ready = False
try:
    if indexer.setup_index(data_loader):
        index_ready = True
        logger.info("Index is ready for queries.")
    else:
        logger.warning("Index setup failed. Web app will show not ready status.")
except Exception as e:
    logger.error(f"Error during index setup: {e}")

@app.route('/')
def home():
    return render_template('index.html', index_ready=index_ready)

@app.route('/query', methods=['POST'])
def query():
    if not index_ready:
        return render_template('index.html', index_ready=index_ready, error="Index is not ready. Please check logs.")

    user_query = request.form.get('query', '').strip()
    if not user_query:
        return render_template('index.html', index_ready=index_ready, error="Please enter a query.")

    try:
        result_dict = query_engine.query(user_query)

        # Extract data from the dictionary
        summary = result_dict.get('summary', '')
        sources = result_dict.get('sources', [])
        snippets = result_dict.get('snippets', {})

        return render_template('index.html', index_ready=index_ready, summary=summary, sources=sources, snippets=snippets)
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        return render_template('index.html', index_ready=index_ready, error="An error occurred while processing your query.")

@app.route('/pdf/<filename>')
def serve_pdf(filename):
    try:
        return send_from_directory('pdf', filename)
    except FileNotFoundError:
        return "File not found", 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
