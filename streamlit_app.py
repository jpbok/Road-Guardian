import streamlit as st
from backend.rag_model import RAGModel  # Import the RAGModel class
import os  # Import os for file operations

# Initialize RAGModel for document retrieval and Q&A
openai_api_key = st.text_input("Enter your OpenAI API Key", type="password")

if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="ℹ️")
else:
    rag_model = RAGModel(openai_api_key=openai_api_key)
    
    # Load and chunk the PDFs in the 'documents' folder
    document_folder = "documents"  # Path to your folder with PDFs
    st.write("Loading theory documents...")
    pdf_text_chunks = rag_model.doc_retriever.docs

    # Show feedback to the user about PDF loading
    if pdf_text_chunks:
        st.success(f"Loaded {len(pdf_text_chunks)} documents from the PDFs.")
    else:
        st.error("No PDF chunks were loaded. Please check the documents folder and try again.")

    st.title("Road Guardian Chatbot")
    st.write("Welcome to Road Guardian! This chatbot helps learner drivers prepare for their driving test by summarizing key theory points and test preparation tips.")

    # Initialize session state for chat messages
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "You are a chatbot that assists learner drivers by summarizing driving theory, providing test preparation tips, and explaining test results."}
        ]

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input for chat
    if prompt := st.chat_input("Ask your driving theory or test-related question here..."):
        # Store and display the current prompt
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response using OpenAI API and the RAG model
        response_text = rag_model.answer_question(prompt)
        
        # Stream and display assistant's response
        with st.chat_message("assistant"):
            st.markdown(response_text)
        
        st.session_state.messages.append({"role": "assistant", "content": response_text})

    # Loading PDFs from the documents folder
    st.write("Loading PDFs from the documents folder...")
    if os.path.exists(document_folder):
        pdf_files = [f for f in os.listdir(document_folder) if f.endswith(".pdf")]
        if pdf_files:
            st.write(f"Found {len(pdf_files)} PDFs:")
            for pdf_file in pdf_files:
                st.write(f"- {pdf_file}")
        else:
            st.error("No PDFs found in the folder.")
    else:
        st.error(f"Folder not found: {document_folder}")
