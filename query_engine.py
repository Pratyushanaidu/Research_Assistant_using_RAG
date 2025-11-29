# /home/kamal/doc_finder/ai_app/query_engine.py
import logging
import os
import pickle
from typing import List, Optional
from langchain_core.documents import Document
from indexer import Indexer
from llm_handler import LLMHandler
from data_loader import DataLoader

logger = logging.getLogger(__name__)

class QueryEngine:
    def __init__(self, indexer: Indexer, llm_handler: LLMHandler, data_loader: DataLoader):
        self.indexer = indexer
        self.llm_handler = llm_handler
        self.data_loader = data_loader
        self.all_docs = []
        self._load_or_create_index()
        logger.info(f"QueryEngine initialized with {len(self.all_docs)} PDFs.")

    def _load_or_create_index(self):
        """Load existing index or create new one from PDFs."""
        index_file = "all_docs.pkl"
        if os.path.exists(index_file):
            logger.info("Loading existing PDF documents from disk...")
            with open(index_file, "rb") as f:
                self.all_docs = pickle.load(f)
            logger.info(f"Loaded {len(self.all_docs)} PDFs from {index_file}.")
        else:
            logger.info("No saved PDFs found. Loading and saving PDFs...")
            self.all_docs = self.data_loader.load_pdfs()
            with open(index_file, "wb") as f:
                pickle.dump(self.all_docs, f)
            logger.info(f"Saved {len(self.all_docs)} PDFs to {index_file}.")

    # get_relevant_docs remains structurally similar, but the 'docs' it returns
    # now represent whole PDFs based on the modified DataLoader.
    def get_relevant_docs(self, query: str) -> List[Document]:
        """
        Queries the index for documents (representing PDFs) most similar to the query.
        Returns a list of Document objects, where each Document's metadata contains the source PDF filename.
        """
        logger.debug(f"Searching index for PDFs relevant to query: '{query}'")
        if self.indexer.vectorstore is None:
             logger.error("Cannot search: Index is not loaded in the Indexer.")
             raise ValueError("Index not loaded or created.")

        try:
            # Search returns Document objects whose embeddings (based on full PDF text) are similar
            relevant_pdf_docs: List[Document] = self.indexer.search(query)
            logger.info(f"Indexer search returned {len(relevant_pdf_docs)} potentially relevant PDF documents for query: '{query}'.")
            if not relevant_pdf_docs:
                 logger.warning(f"Indexer search returned no relevant PDF documents for query: '{query}'")
            else:
                 # Log the filenames found
                 sources = [doc.metadata.get('source', 'Unknown Source') for doc in relevant_pdf_docs]
                 logger.debug(f"Found potentially relevant PDF sources: {sources}")
            return relevant_pdf_docs
        except Exception as e:
            logger.error(f"An unexpected error occurred during indexer.search for query '{query}': {e}", exc_info=True)
            return [] # Return empty list on unexpected search errors


    def query(self, user_query: str) -> dict:
        """
        Loads all PDF documents, extracts content, then asks the LLM
        to provide an ordered answer as a numbered list of key points.
        Returns a dictionary with summary, sources, and snippets.
        """
        logger.info(f"Processing query to provide ordered answer from all PDFs: '{user_query}'")
        try:
            # 1. Use pre-loaded PDF documents
            all_pdf_docs = self.all_docs

            # 2. Extract filenames and content
            if not all_pdf_docs:
                logger.warning(f"No PDF documents found for query: '{user_query}'")
                return {
                    'summary': "I could not find any PDF files to process.",
                    'sources': [],
                    'snippets': {}
                }
            else:
                # Get the list of all source filenames from the metadata
                all_filenames = [doc.metadata.get('source', 'Unknown Source') for doc in all_pdf_docs]
                # Remove duplicates and sort for consistent prompting
                unique_filenames = sorted(list(set(all_filenames)))

                # Extract snippets (first 1000 characters from each doc's content for more context)
                snippets = {}
                full_content = ""
                for doc in all_pdf_docs:
                    filename = doc.metadata.get('source', 'Unknown Source')
                    content = doc.page_content[:1000] + "..." if len(doc.page_content) > 1000 else doc.page_content
                    snippets[filename] = content
                    full_content += f"\n\nFrom {filename}:\n{content}"

                logger.info(f"Processing information from all PDF files: {unique_filenames}")

                # 3. Construct the prompt for the LLM to generate an ordered answer
                prompt = f"""Based on the user's query "{user_query}", analyze the content from all the provided PDF documents and provide an ordered answer as a numbered list of key points. Ensure the answer is comprehensive by considering information from every document.

Provide the ordered answer as a numbered list (1., 2., 3., etc.) of key points directly addressing the query. Do not include section headers like "Definition" or "Sources" in the response body. List all source documents at the end, numbered.

PDF Content:
{full_content}

Ordered Answer:"""
                logger.info("Sending prompt to LLM to generate ordered answer.")
                # Handle potential object response from LLM (like ChatGroq)
                response_obj = self.llm_handler.generate_response(prompt)
                response_text = response_obj.content if hasattr(response_obj, 'content') else str(response_obj)

                logger.info("Received ordered answer response from LLM.")
                return {
                    'summary': response_text.strip(),
                    'sources': unique_filenames,
                    'snippets': snippets
                }

        except ValueError as e: # Catch error if index not loaded during get_relevant_docs
             logger.error(f"Error during index search: {e}")
             return {
                 'suggestion': "Error: The document index is not available. Please ensure it has been created or loaded.",
                 'sources': [],
                 'snippets': {}
             }
        except Exception as e:
            logger.error(f"An unexpected error occurred during query processing for query '{user_query}': {e}", exc_info=True)
            return {
                'suggestion': "An unexpected error occurred while processing your query.",
                'sources': [],
                'snippets': {}
            }
