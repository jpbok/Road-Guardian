import streamlit as st
from openai import OpenAI
from rag_model import RAGModel  # Import the RAG model

# Initialize RAG model for document retrieval
rag_model = RAGModel()

# Load your theory book and checklist (for demonstration purposes, we use sample text).
theory_text = """
Driving through a junction requires you to check all directions for oncoming vehicles.
Ensure that you follow the traffic lights and give way to pedestrians.
Speed limits must always be observed, especially in school zones.
"""
checklist_text = """
Ensure seatbelt is fastened. Check rear-view mirrors before moving. Signal clearly before turning.
"""

# Chunk the documents and build the index
rag_model.build_index(rag_model.chunk_text(theory_text) + rag_model.chunk_text(checklist_text))

# Streamlit app layout
st.title("🚗 Road Guardian Chatbot")
st.write(
    "Welcome to Road Guardian! This chatbot helps learner drivers prepare for their driving test by summarizing key theory points and test preparation tips."
)

# Ask user for their OpenAI API key
openai_api_key = st.text_input("Enter your OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    # Create an OpenAI client
    client = OpenAI(api_key=openai_api_key)

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

        # Retrieve relevant documents using RAG model
        relevant_docs = rag_model.retrieve_documents(prompt)

        # Generate response using OpenAI API, including the relevant documents
        response = client.completions.create(
            model="gpt-3.5-turbo",
            prompt=f"Based on the following documents, answer the user's question: {relevant_docs}.\n\nQuestion: {prompt}",
        )

        # Stream and display assistant's response
        with st.chat_message("assistant"):
            response_text = response['choices'][0]['text']
            st.markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})
