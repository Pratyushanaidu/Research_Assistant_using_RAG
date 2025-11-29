from flask import Flask, request, render_template  
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
