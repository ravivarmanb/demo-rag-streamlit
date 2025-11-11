import os
import streamlit as st
from google.generativeai import configure, GenerativeModel
import chromadb
from chromadb.config import Settings
from pypdf import PdfReader
from dotenv import load_dotenv
import pandas as pd
from docx import Document

# Load environment
load_dotenv()

def load_documents(folder_path):
    """Load and process documents from local folder"""
    documents = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        if filename.endswith('.pdf'):
            reader = PdfReader(file_path)
            text = ' '.join([page.extract_text() for page in reader.pages])
            documents.append({'text': text, 'source': filename})
        
        elif filename.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            documents.append({'text': text, 'source': filename})
        
        elif filename.endswith(('.docx', '.doc')):
            doc = Document(file_path)
            text = '\n'.join([para.text for para in doc.paragraphs])
            documents.append({'text': text, 'source': filename})
        
        elif filename.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file_path)
            text = df.to_string(index=False)
            documents.append({'text': text, 'source': filename})
    
    return documents

def setup_chroma(documents):
    """Setup ChromaDB with documents"""
    client = chromadb.PersistentClient(path="chroma_db")
    
    collection = client.get_or_create_collection(name="knowledge_base")
    
    # Add documents if not already present
    if collection.count() == 0:
        ids = [str(i) for i in range(len(documents))]
        texts = [doc['text'] for doc in documents]
        metadatas = [{'source': doc['source']} for doc in documents]
        collection.add(ids=ids, documents=texts, metadatas=metadatas)
    
    return collection

def rag_query(collection, query, n_results=3):
    """Query ChromaDB for relevant documents"""
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    return results

def main():
    st.title('RAG Chat with Gemini 2.5 Flash')
    
    # Initialize Gemini
    configure(api_key=os.getenv('GEMINI_API_KEY'))
    model = GenerativeModel('gemini-2.5-flash')
    
    # Setup RAG
    knowledge_folder = "local knowledge"
    if not os.path.exists(knowledge_folder):
        os.makedirs(knowledge_folder)
    
    documents = load_documents(knowledge_folder)
    collection = setup_chroma(documents)
    
    # Chat interface
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if prompt := st.chat_input("Ask me anything"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # First try RAG
        rag_results = rag_query(collection, prompt)
        if rag_results['documents'] and rag_results['documents'][0]:
            context = '\n'.join(rag_results['documents'][0])
            # Check if context is meaningful (not empty or just whitespace)
            if context.strip() and len(context.strip()) > 50:
                response = model.generate_content(f"Using the provided context, answer the question. If the context doesn't contain relevant information, say so and use your general knowledge.\n\nContext: {context}\n\nQuestion: {prompt}")
            else:
                # Fallback to model's general knowledge
                response = model.generate_content(f"Answer this question using your general knowledge: {prompt}")
        else:
            # Fallback to model's general knowledge
            response = model.generate_content(f"Answer this question using your general knowledge: {prompt}")
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})

if __name__ == "__main__":
    main()
