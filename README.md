# RAG Chat with Gemini 2.5 Flash

A Streamlit-based RAG (Retrieval-Augmented Generation) chat application that uses Google's Gemini 2.5 Flash model to answer questions based on local documents.

## Features

- 📚 **Multi-format document support**: PDF, TXT, DOCX, XLSX
- 🔍 **RAG-powered responses**: Uses ChromaDB for document retrieval
- 🤖 **Smart fallback**: Uses model's general knowledge when RAG doesn't find relevant information
- 💬 **Interactive chat interface**: Clean Streamlit chat UI
- 🧠 **Vector database**: ChromaDB for efficient document similarity search

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your environment variables:
   - Copy `.env.example` to `.env`
   - Add your Gemini API key: `GEMINI_API_KEY=your_api_key_here`

## Usage

1. Place your documents in the `local knowledge/` folder
2. Run the app:
   ```bash
   streamlit run app.py
   ```
3. Open your browser and go to `http://localhost:8501`
4. Start chatting with your documents!

## How it Works

1. **Document Loading**: The app loads and processes documents from the `local knowledge/` folder
2. **Vector Storage**: Documents are converted to embeddings and stored in ChromaDB
3. **Query Processing**: When you ask a question, the app:
   - Searches for relevant documents in the vector database
   - If relevant content is found, uses it as context for the AI
   - If no relevant content is found, falls back to the model's general knowledge
4. **Response Generation**: Gemini 2.5 Flash generates contextual responses

## Supported Document Types

- PDF files (.pdf)
- Text files (.txt)
- Word documents (.docx, .doc)
- Excel files (.xlsx, .xls)

## Requirements

- Python 3.8+
- Google Gemini API key
- See `requirements.txt` for package dependencies

## License

MIT License
