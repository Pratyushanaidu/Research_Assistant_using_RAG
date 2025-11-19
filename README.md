# Research Assistant-using RAG
Research Assistant is a sophisticated web application that enables users to upload PDF documents, index them for efficient semantic search, and interact with an AI-powered chatbot to ask questions about the content. Built with Flask and powered by vector embeddings and Large Language Models (LLMs), it provides an intuitive interface for document exploration and knowledge discovery.

## 🌟 Features

### Core Functionality
- *📄 PDF Document Management*: Upload, view, and download PDF files with automatic indexing
- *🔍 Semantic Search*: Vector-based similarity search for finding relevant content
- *🤖 AI Chatbot*: Ask natural language questions about your documents
- *📊 Document Analytics*: View statistics about uploaded documents and index status
- *🔐 User Authentication*: Secure login and registration system
- *📱 Responsive UI*: Clean, modern web interface that works on all devices

### Advanced Features
- *Multi-Method Search*: Support for different search algorithms (vector, keyword, hybrid)
- *Structured Responses*: Chatbot answers formatted in clear sections
- *Citation Support*: Source attribution for search results
- *Health Monitoring*: System status and component health checks
- *Error Recovery*: Graceful handling of LLM failures and system issues
- *Batch Processing*: Upload multiple documents simultaneously

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git (for cloning the repository)

### Installation

1. *Clone the repository*
   bash
   git clone https://github.com/Pratyushanaidu/Research-Assistant.git
   cd doc-finder
   

2. *Create a virtual environment*
   bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   

3. *Install dependencies*
   bash
   pip install -r requirements.txt
   

4. *Configure environment variables* (optional)
   bash
   export FLASK_SECRET_KEY="your-secret-key-here"
   

5. *Run the application*
   bash
   python app.py
   

6. *Open your browser*
   Navigate to http://localhost:5000 and log in with:
   - Username: admin
   - Password: password

## 📖 Usage

### Basic Workflow

1. *Login*: Use the default credentials or register a new account
2. *Upload Documents*: Go to the Upload page and select PDF files
3. *Wait for Indexing*: The system automatically processes and indexes your documents
4. *Ask Questions*: Use the Chatbot to ask questions about your documents
5. *Search Documents*: Use the search functionality for specific queries
6. *View Results*: Explore formatted answers with source citations

### Example Usage

python
# The application handles everything through the web interface
# No additional coding required for basic usage


## ⚙ Configuration

### Environment Variables
- FLASK_SECRET_KEY: Secret key for Flask sessions (auto-generated if not set)

### Configuration File (config.py)
python
# Key settings you can modify
PDF_DIRECTORY = "pdfs/"          # Where uploaded PDFs are stored
INDEX_DIRECTORY = "index/"       # Where vector index is saved
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Sentence transformer model


### LLM Integration (Optional)
To enable AI features, configure your LLM provider:
- Set API keys for OpenAI, Anthropic, or other providers
- The system gracefully degrades if LLM is unavailable

## 🏗 Architecture

### Core Components
- *Flask App*: Web framework and routing
- *DataLoader*: PDF text extraction and processing
- *Embedder*: Vector embedding generation
- *Indexer*: FAISS vector database management
- *QueryEngine*: Search orchestration and LLM integration
- *LLMHandler*: Large Language Model interface

### Data Flow

PDF Upload → Text Extraction → Vector Embedding → FAISS Index → Query → LLM → Formatted Response


## 📚 API Endpoints

### Public Endpoints
- GET /: Home page (requires login)
- GET /login: Login page
- POST /login: Process login
- GET /register: Registration page
- POST /register: Process registration
- GET /logout: Logout

### Protected Endpoints (require authentication)
- GET /upload: Document upload page
- POST /upload_documents: Handle file uploads
- GET /chatbot: AI chatbot interface
- POST /ask_chatbot: Process chatbot questions
- GET /documents: Document listing
- GET /query: Search interface
- POST /query: Process search queries
- GET /health: System health check

### File Serving
- GET /pdfs/<filename>: Serve PDF files
- GET /download_pdf/<filename>: Download PDF files

## 🔧 Development

### Project Structure

doc-finder/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── data_loader.py        # PDF processing
├── embedder.py           # Text embeddings
├── indexer.py            # Vector indexing
├── query_engine.py       # Search orchestration
├── llm_handler.py        # LLM integration
├── templates/            # HTML templates
│   ├── index.html
│   ├── login.html
│   ├── upload.html
│   ├── chatbot.html
│   └── ...
├── static/               # CSS, JS, images
├── requirements.txt      # Python dependencies
└── README.md            # This file


### Running Tests
bash
# Add your test commands here
python -m pytest tests/


### Contributing
1. Fork the repository
2. Create a feature branch (git checkout -b feature/amazing-feature)
3. Commit your changes (git commit -m 'Add amazing feature')
4. Push to the branch (git push origin feature/amazing-feature)
5. Open a Pull Request

## 📋 Requirements

### Core Dependencies
- Flask>=2.0.0
- faiss-cpu>=1.7.0
- sentence-transformers>=2.2.0
- PyPDF2>=3.0.0
- werkzeug>=2.0.0

### Optional Dependencies (for AI features)
- openai>=1.0.0
- anthropic>=0.5.0

See requirements.txt for the complete list.

## 🐛 Troubleshooting

### Common Issues

*"Document index is not ready"*
- Upload some PDF documents first
- Wait for indexing to complete
- Check the logs for any errors

*"LLM features not working"*
- Ensure you have set up API keys for your LLM provider
- Check that the LLM service is accessible
- The system will work with basic search even without LLM

*"Upload fails"*
- Ensure files are valid PDFs
- Check file size limits
- Verify write permissions on the pdfs/ directory

### Debug Mode
Run with debug logging:
bash
export FLASK_ENV=development
python app.py

## 🙏 Acknowledgments

- Built with [Flask](https://flask.palletsprojects.com/)
- Vector search powered by [FAISS](https://github.com/facebookresearch/faiss)
- Embeddings from [Sentence Transformers](https://www.sbert.net/)
- UI inspired by modern web design principles

## 📞 Support

If you encounter issues or have questions:
1. Check the troubleshooting section above
2. Review the logs for error messages
3. Open an issue on GitHub with detailed information

---

*Happy Document Exploring! 📚🤖*
