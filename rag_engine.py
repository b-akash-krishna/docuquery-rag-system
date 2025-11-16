import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

load_dotenv()

class RAGEngine:
    def __init__(self):
        self.groq_key = os.getenv("GROQ_API_KEY")
        if not self.groq_key:
            raise ValueError("GROQ_API_KEY not found in .env file")
        
        print("Loading embedding model...")
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )
        print("✅ Embeddings loaded!")
        
        print("Initializing Groq LLM...")
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.2,  # Lower temperature for more focused answers
            groq_api_key=self.groq_key,
            max_tokens=1024
        )
        print("✅ Groq LLM ready!")
        
        self.vectorstore = None
        
    def process_document(self, pdf_path):
        """Process PDF with optimized chunking"""
        print("Loading PDF...")
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()
        print(f"✅ Loaded {len(documents)} pages")
        
        # IMPROVED: Larger chunks with more overlap for better context
        print("Chunking text...")
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1500,  # Increased from 1000
            chunk_overlap=300,  # Increased from 200
            separators=["\n\n", "\n", ". ", " ", ""]  # Better separators
        )
        chunks = splitter.split_documents(documents)
        print(f"✅ Created {len(chunks)} chunks")
        
        print("Creating embeddings...")
        self.vectorstore = FAISS.from_documents(chunks, self.embeddings)
        print("✅ Document processed successfully!")
        
        return len(chunks)
    
    def query(self, question):
        """Query with improved retrieval and prompting"""
        if not self.vectorstore:
            raise ValueError("No document loaded!")
        
        # IMPROVED: Get more relevant chunks with better scoring
        docs = self.vectorstore.similarity_search(
            question, 
            k=4,  # Get 4 chunks instead of 3
            fetch_k=10  # Consider more candidates
        )
        
        # Create comprehensive context
        context = "\n\n---\n\n".join([
            f"[From Page {doc.metadata.get('page', 'N/A') + 1}]\n{doc.page_content}" 
            for doc in docs
        ])
        
        # IMPROVED: Much better prompt with explicit instructions
        prompt = f"""You are a precise AI assistant answering questions about a document.

CRITICAL RULES:
1. Read the user's question EXACTLY as written
2. Answer ONLY that specific question - do not make up different questions
3. Use ONLY the information from the context below
4. If the context doesn't clearly answer the question, say: "Based on the provided document sections, I don't have enough specific information to answer this question accurately."
5. Be direct and concise

===== DOCUMENT CONTEXT =====
{context}
================================

USER'S QUESTION: {question}

ANSWER (be direct and accurate):"""
        
        try:
            response = self.llm.invoke(prompt)
            answer = response.content.strip()
            
            # Clean up any weird formatting
            if answer.startswith(":"):
                answer = answer[1:].strip()
            
            return {
                "answer": answer,
                "source_documents": docs
            }
        except Exception as e:
            error_msg = str(e).lower()
            if "rate" in error_msg or "limit" in error_msg:
                return {
                    "answer": "⚠️ Rate limit reached. Please wait 60 seconds.",
                    "source_documents": docs
                }
            else:
                return {
                    "answer": f"⚠️ Error: {str(e)[:100]}",
                    "source_documents": docs
                }

if __name__ == "__main__":
    try:
        print("Initializing RAG Engine with Groq...")
        engine = RAGEngine()
        print("✅ RAG Engine initialized successfully!")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
