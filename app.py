import streamlit as st
import os
import tempfile
from rag_engine import RAGEngine
import time

# Page configuration
st.set_page_config(
    page_title="DocuQuery - AI Document Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS
st.markdown("""
    <style>
    /* Main background and fonts */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
    }
    
    .stApp {
        background: transparent;
    }
    
    /* Chat message styling */
    .chat-message {
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        animation: fadeIn 0.5s;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        margin-left: 20%;
        border-bottom-right-radius: 5px;
    }
    
    .user-message * {
        color: white !important;
    }
    
    .bot-message {
        background: #f8f9fa;
        border: 2px solid #e9ecef;
        margin-right: 20%;
        border-bottom-left-radius: 5px;
        color: #212529 !important;
    }
    
    .bot-message * {
        color: #212529 !important;
    }
    
    .message-label {
        font-weight: 700;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: #212529 !important;
    }
    
    .message-content {
        font-size: 1rem;
        line-height: 1.6;
        white-space: pre-wrap;
        color: #212529 !important;
    }
    
    /* Stats cards */
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0;
    }
    
    .stat-label {
        font-size: 0.9rem;
        opacity: 0.9;
        margin-top: 0.5rem;
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Success/Error messages */
    .success-message {
        background: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
        color: #155724 !important;
    }
    
    .error-message {
        background: #f8d7da;
        border-left: 4px solid #dc3545;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
        color: #721c24 !important;
    }
    
    /* Headers */
    h1 {
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        font-size: 3rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    h2, h3 {
        color: white !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Divider */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
        margin: 2rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'rag_engine' not in st.session_state:
    st.session_state.rag_engine = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'document_processed' not in st.session_state:
    st.session_state.document_processed = False
if 'chunks_count' not in st.session_state:
    st.session_state.chunks_count = 0
if 'doc_name' not in st.session_state:
    st.session_state.doc_name = ""
if 'pending_question' not in st.session_state:
    st.session_state.pending_question = None

# Header
st.markdown("# 📚 DocuQuery")
st.markdown("<p style='color: white; font-size: 1.2rem; margin-top: -1rem;'>AI-Powered Document Intelligence</p>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 📄 Document Upload")
    
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=['pdf'],
        help="Upload a PDF document to analyze",
        label_visibility="collapsed"
    )
    
    if uploaded_file:
        if st.button("🚀 Process Document", type="primary"):
            with st.spinner("🔄 Processing your document..."):
                try:
                    # Save uploaded file temporarily
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                        tmp_file.write(uploaded_file.read())
                        tmp_path = tmp_file.name
                    
                    # Initialize RAG engine if not exists
                    if st.session_state.rag_engine is None:
                        st.session_state.rag_engine = RAGEngine()
                    
                    # Process document
                    chunks_count = st.session_state.rag_engine.process_document(tmp_path)
                    
                    st.session_state.document_processed = True
                    st.session_state.chunks_count = chunks_count
                    st.session_state.doc_name = uploaded_file.name
                    
                    # Clean up temp file
                    os.unlink(tmp_path)
                    
                    st.markdown("""
                        <div class="success-message">
                            ✅ Document processed successfully!
                        </div>
                    """, unsafe_allow_html=True)
                    time.sleep(1)
                    st.rerun()
                    
                except Exception as e:
                    st.markdown(f"""
                        <div class="error-message">
                            ❌ Error: {str(e)}
                        </div>
                    """, unsafe_allow_html=True)
    
    # Document stats
    if st.session_state.document_processed:
        st.markdown("---")
        st.markdown("### 📊 Document Stats")
        
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{st.session_state.chunks_count}</div>
                <div class="stat-label">Text Chunks</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{len(st.session_state.chat_history) // 2}</div>
                <div class="stat-label">Questions Asked</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"**📎 Document:** `{st.session_state.doc_name}`")
    
    st.markdown("---")
    
    # Clear conversation
    if st.button("🗑️ Clear Conversation"):
        st.session_state.chat_history = []
        st.rerun()
    
    # Info section
    st.markdown("---")
    st.markdown("### 💡 How it Works")
    st.markdown("""
    1. **Upload** a PDF document
    2. **Process** to create embeddings
    3. **Ask** questions naturally
    4. **Get** AI-powered answers with sources
    """)
    
    st.markdown("### ⚡ Powered by")
    st.markdown("""
    - 🤖 **Groq AI** (Llama 3.3)
    - 🔗 **LangChain** RAG
    - 🔍 **FAISS** Vector DB
    - 🎨 **Streamlit** UI
    """)

# Main content area
if st.session_state.document_processed:
    # Chat interface
    st.markdown("### 💬 Chat with Your Document")
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message['role'] == 'user':
            st.markdown(f"""
                <div class="chat-message user-message">
                    <div class="message-label">👤 You</div>
                    <div class="message-content">{message['content']}</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="chat-message bot-message">
                    <div class="message-label">🤖 AI Assistant</div>
                    <div class="message-content">{message['content']}</div>
                </div>
            """, unsafe_allow_html=True)
    
    # Question input
    with st.form(key='question_form', clear_on_submit=True):
        user_question = st.text_input(
            "Ask a question about your document:",
            value=st.session_state.pending_question if st.session_state.pending_question else "",
            placeholder="e.g., What are the main findings in this document?",
            label_visibility="collapsed"
        )
        submit_button = st.form_submit_button("🔍 Ask", use_container_width=True)
    
    # Process question
    if submit_button and user_question:
        # Clear pending question
        st.session_state.pending_question = None
        
        # Add user message
        st.session_state.chat_history.append({
            'role': 'user',
            'content': user_question
        })
        
        # Get answer
        with st.spinner("🤔 Thinking..."):
            try:
                response = st.session_state.rag_engine.query(user_question)
                answer = response['answer']
                sources = response['source_documents']
                
                # Format response
                full_response = f"**Question:** {user_question}\n\n**Answer:**\n{answer}\n\n"
                
                if sources:
                    full_response += "📚 **Sources:**"
                    for i, doc in enumerate(sources[:3], 1):
                        page = doc.metadata.get('page', 'N/A')
                        preview = doc.page_content[:150].replace('\n', ' ').strip()
                        full_response += f"\n• **Page {page + 1}:** {preview}..."
                
                st.session_state.chat_history.append({
                    'role': 'assistant',
                    'content': full_response
                })
                
                st.rerun()
                
            except Exception as e:
                error_msg = f"⚠️ Error: {str(e)}"
                st.session_state.chat_history.append({
                    'role': 'assistant',
                    'content': error_msg
                })
                st.rerun()
    
    # Example questions (only show if no chat history)
    if len(st.session_state.chat_history) == 0:
        st.markdown("### 💭 Try These Questions:")
        
        example_questions = [
            "What is this document about?",
            "Summarize the main points",
            "What are the key findings?",
            "List the important concepts"
        ]
        
        cols = st.columns(2)
        for i, question in enumerate(example_questions):
            with cols[i % 2]:
                if st.button(f"💡 {question}", key=f"example_{i}", use_container_width=True):
                    # Set pending question and trigger rerun
                    st.session_state.pending_question = question
                    st.session_state.chat_history.append({
                        'role': 'user',
                        'content': question
                    })
                    
                    # Get answer immediately
                    with st.spinner("🤔 Thinking..."):
                        try:
                            response = st.session_state.rag_engine.query(question)
                            answer = response['answer']
                            sources = response['source_documents']
                            
                            # Format response
                            full_response = f"**Question:** {question}\n\n**Answer:**\n{answer}\n\n"
                            
                            if sources:
                                full_response += "📚 **Sources:**"
                                for j, doc in enumerate(sources[:3], 1):
                                    page = doc.metadata.get('page', 'N/A')
                                    preview = doc.page_content[:150].replace('\n', ' ').strip()
                                    full_response += f"\n• **Page {page + 1}:** {preview}..."
                            
                            st.session_state.chat_history.append({
                                'role': 'assistant',
                                'content': full_response
                            })
                            
                            st.rerun()
                            
                        except Exception as e:
                            error_msg = f"⚠️ Error: {str(e)}"
                            st.session_state.chat_history.append({
                                'role': 'assistant',
                                'content': error_msg
                            })
                            st.rerun()

else:
    # Welcome screen
    st.info("👈 **Get started:** Upload a PDF document using the sidebar to begin!")
    
    st.markdown("""
        ### 🎯 What is DocuQuery?
        
        DocuQuery is an intelligent RAG (Retrieval-Augmented Generation) system that helps you:
        - 📖 Understand complex documents quickly
        - 🔍 Find specific information instantly
        - 💡 Get contextual answers to your questions
        - 📚 Extract insights with source citations
        
        ### ✨ Perfect For:
        - Research papers and academic documents
        - Business reports and technical documentation
        - Study materials and learning resources
        - Any PDF document you need to analyze
    """)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: white; padding: 1rem;'>
        <strong>Built with ❤️ for EONVERSE AI Internship Challenge</strong><br/>
        <small>Powered by Groq AI • LangChain • FAISS • Streamlit</small>
    </div>
""", unsafe_allow_html=True)
