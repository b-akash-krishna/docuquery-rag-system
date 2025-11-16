# 📚 DocuQuery - AI-Powered Document Intelligence

> An intelligent RAG (Retrieval-Augmented Generation) system that enables natural language interaction with PDF documents using state-of-the-art AI technology.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![LangChain](https://img.shields.io/badge/LangChain-Latest-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.29-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🎯 Overview

DocuQuery transforms how you interact with documents. Upload any PDF and ask questions in natural language to receive accurate, context-aware answers with source citations—all powered by advanced AI and semantic search.

**Built for the EONVERSE AI Internship Challenge**

---

## ✨ Features

- **🚀 Intelligent Q&A**: Ask questions about your documents in natural language
- **📄 PDF Processing**: Automatic text extraction and intelligent chunking
- **🔍 Semantic Search**: FAISS-powered vector similarity search
- **🤖 AI-Powered Answers**: Context-aware responses using Groq's Llama 3.3 70B
- **📚 Source Citations**: Every answer includes references to source pages
- **💬 Chat Interface**: Beautiful, intuitive conversation-style UI
- **⚡ Fast & Free**: Local embeddings + free Groq API = no limits
- **🎨 Modern UI**: Responsive Streamlit interface with gradient design

---

## 🏗️ Architecture

```bash
    ┌─────────────┐
    │   PDF File  │
    └──────┬──────┘
           │
           ▼
┌─────────────────────────────┐
│   Document Loader (PyPDF)   │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│       Text Chunking         │
│  (RecursiveCharacterSplit)  │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│      Local Embeddings       │
│   (sentence-transformers)   │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│    Vector Store (FAISS)     │
└──────────┬──────────────────┘
           │
           ▼
      ┌──────────┐
      │  Query   │
      └────┬─────┘
           │
           ▼
┌─────────────────────────────┐
│      Similarity Search      │
│   (Retrieve Top K Chunks)   │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│       LLM Generation        │
│      (Groq Llama 3.3)       │
└──────────┬──────────────────┘
           │
           ▼
      ┌──────────┐
      │  Answer  │ 
      │     +    │
      │  Sources │
      └──────────┘
```

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Frontend** | Streamlit | Interactive web UI |
| **LLM** | Groq (Llama 3.3 70B) | Question answering |
| **Embeddings** | sentence-transformers | Local semantic embeddings |
| **Vector DB** | FAISS | Fast similarity search |
| **Framework** | LangChain | RAG pipeline orchestration |
| **PDF Processing** | PyPDF | Document parsing |
| **Language** | Python 3.12 | Core implementation |

---

## 📦 Installation

### Prerequisites

- Python 3.12 or higher
- Groq API key (free at [console.groq.com](https://console.groq.com))

### Step-by-Step Setup
1. **Clone the repository**
```bash
git clone https://github.com/yourusername/docuquery.git
cd docuquery
```

2. **Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
Create a `.env` file in the project root:
GROQ_API_KEY=your_groq_api_key_here
```

5. **Run the application**
```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`

---

## 🚀 Usage

### Basic Workflow

1. **Upload a PDF**: Click "Choose a PDF file" in the sidebar
2. **Process Document**: Click "🚀 Process Document" button
3. **Ask Questions**: Type your question or click example questions
4. **Get Answers**: Receive AI-powered answers with source citations

### Example Questions

- "What is this document about?"
- "Summarize the main points"
- "What are the key findings?"
- "Explain the methodology used"

### Supported Documents

✅ Research papers  
✅ Business reports  
✅ Technical documentation  
✅ Study materials  
✅ Any well-structured PDF

---

## 📂 Project Structure
```bash
docuquery/
├── app.py # Streamlit UI application
├── rag_engine.py # Core RAG logic
├── requirements.txt # Python dependencies
├── .env # Environment variables (create this)
├── .gitignore # Git ignore rules
├── README.md # This file
├── REFLECTION.md # Project reflection document
└── assets/ # Screenshots and media
├── demo
```

---

## 🎨 Key Components

### RAG Engine (`rag_engine.py`)
```bash
class RAGEngine:
- process_document() # Load, chunk, embed, store 
- query() # Retrieve context and generate answer
```

**Features:**
- Optimized chunk size (1500 chars) with 300-char overlap
- Local embeddings (no API limits)
- Retrieves top 4 relevant chunks
- Error handling for rate limits

### Streamlit App (`app.py`)

**Features:**
- Modern gradient UI design
- Real-time chat interface
- Document statistics
- Example questions
- Session state management
- Professional error handling

---

## ⚙️ Configuration

### Adjustable Parameters

In `rag_engine.py`:
```bash
Chunking parameters
chunk_size=1500 # Size of text chunks
chunk_overlap=300 # Overlap between chunks

Retrieval parameters
k=4 # Number of chunks to retrieve
fetch_k=10 # Candidate chunks to consider

LLM parameters
temperature=0.2 # Lower = more focused
ma_tokens=1024 # Maximum response length
```

---

## 🧪 Testing

### Manual Testing

1. Upload test PDF (e.g., EONVERSE challenge document)
2. Ask: "What is this document about?"
3. Verify:
   - Answer is accurate
   - Sources are cited
   - Page numbers are correct

### Test PDFs

Included in `/test_data/`:
- Simple structured documents ✅
- Technical papers ✅
- Business reports ✅

---

## 🐛 Known Limitations

### Document Structure Sensitivity

**Challenge Identified:**
Dense Q&A formatted documents with repetitive patterns may produce less accurate results due to semantic similarity confusion.

**Works Best With:**
- Research papers
- Technical documentation
- Business reports
- Structured guides

**Potential Solutions (Future Work):**
- Document-type detection preprocessing
- Hybrid search (semantic + keyword)
- Metadata enrichment for Q&A documents
- Proposition-based chunking

---

## 🚀 Future Enhancements

- [ ] Multi-document querying
- [ ] Document comparison feature
- [ ] Export conversation history
- [ ] Support for more file formats (DOCX, TXT)
- [ ] Advanced filters (date range, topic)
- [ ] Conversation memory across sessions
- [ ] Custom model selection
- [ ] Deployment to cloud (Streamlit Cloud/Hugging Face Spaces)

---

## 📊 Performance

| Metric | Value |
|--------|-------|
| Average Response Time | 2-4 seconds |
| Supported PDF Size | Up to 50MB |
| Concurrent Users | Single session |
| Embedding Speed | ~100 chunks/minute |
| Groq API Limit (Free) | 14,400 requests/day |

---

## 🤝 Contributing

This is a solo project built for the EONVERSE AI Internship Challenge. However, feedback and suggestions are welcome!

---

## 📄 License

MIT License - Feel free to use this project for learning and development.

---

## 👨‍💻 Author

**B AKASH KRISHNA**  
AI/ML Engineering Student  
Built for: EONVERSE AI Internship Challenge

- GitHub: [@b-akash-krishna](https://github.com/b-akash-krishna)
- LinkedIn: [B AKASH KRISHNA](https://www.linkedin.com/in/b-akash-krishna/)
- Email: b.akashkrishna27@gmail.com

---

## 🙏 Acknowledgments

- **EONVERSE** for the internship challenge opportunity
- **Groq** for providing free, fast LLM API
- **LangChain** for the excellent RAG framework
- **Streamlit** for the intuitive UI framework

---

## 📚 References

- [LangChain Documentation](https://python.langchain.com/)
- [Groq API Docs](https://console.groq.com/docs)
- [FAISS Documentation](https://github.com/facebookresearch/faiss)
- [Streamlit Documentation](https://docs.streamlit.io/)

---

**Built with ❤️ using AI and Open Source Technology**