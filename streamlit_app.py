import streamlit as st
import PyPDF2
import json
from openai import OpenAI
from sentence_transformers import SentenceTransformer, util
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Input for OpenAI API Key
openai_api_key = st.text_input("Enter your OpenAI API Key", type="password")

if not openai_api_key:
    st.info("Please enter your OpenAI API key to continue.")
    st.stop()

# Instantiate OpenAI client
client = OpenAI(api_key=openai_api_key)

# Define document sets for learner drivers and riders
learner_driver_docs = ['documents/chunks/basic_theory_chunk_', 'documents/chunks/final_theory_chunk_']
learner_rider_docs = ['documents/chunks/basic_theory_chunk_', 'documents/chunks/riding_theory_chunk_']

# Option selection: learner driver or rider
option = st.selectbox('Select learner type', ['Learner Driver', 'Learner Rider'])

# Load appropriate metadata
if option == 'Learner Driver':
    metadata_path = 'documents/chunks/driver_metadata.json'
elif option == 'Learner Rider':
    metadata_path = 'documents/chunks/rider_metadata.json'

# Load metadata file
try:
    with open(metadata_path) as f:
        metadata = json.load(f)
except FileNotFoundError:
    st.error(f"Metadata file not found: {metadata_path}")
    st.stop()

# Load the Sentence-Transformers model
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def load_pdf_chunk(chunk_path):
    """Loads a specific chunk of the PDF."""
    try:
        with open(chunk_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
        return text
    except FileNotFoundError:
        st.error(f"File not found: {chunk_path}")
        return ""

def find_relevant_chunk(query):
    """Find the most relevant chunk based on a query."""
    query_embedding = model.encode(query, convert_to_tensor=True)
    best_chunk = None
    highest_similarity = 0

    for chunk in metadata:
        chunk_embedding = model.encode(chunk['summary'], convert_to_tensor=True)
        similarity = util.pytorch_cos_sim(query_embedding, chunk_embedding).item()
        if similarity > highest_similarity:
            highest_similarity = similarity
            best_chunk = chunk

    if best_chunk:
        return best_chunk['path']
    return None

def get_llm_response(chunk_text):
    """Generates a response using the LLM."""
    try:
        messages = [
            {"role": "system", "content": "You are a helpful assistant for driving or riding theory test preparation."},
            {"role": "user", "content": f"Summarize the following text and provide key points relevant for a learner driver/rider:\n\n{chunk_text}"}
        ]
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0,
            max_tokens=300
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Error generating response: {e}")
        return None

def handle_submit():
    query = st.session_state.query_input
    if query:
        chunk_path = find_relevant_chunk(query)
        
        if chunk_path:
            chunk_text = load_pdf_chunk(chunk_path)
            findings_container = st.container()
            with findings_container:
                st.subheader("Findings:")
                st.write(chunk_text)  # Display the original chunk text
            
            llm_response = get_llm_response(chunk_text)  # Get the LLM's response
            if llm_response:
                response_container = st.container()
                with response_container:
                    st.subheader("LLM Response:")
                    st.write(llm_response)  # Display the LLM's response
            else:
                st.write("Failed to generate a response.")
        else:
            st.write("No relevant section found.")

# Main app title and description
st.title("Road Guardian Chatbot")
st.write("""
**Welcome to Road Guardian!**  
This chatbot is your ultimate companion to ace the driving or riding test. We make learning the key theory points simple and fun. 🛣️

### **How it Works:**
1. **Enter Your Query:** Ask anything about driving or riding theory, road signs, or test tips.
2. **Get Quick Summaries:** Receive concise and clear summaries of essential information.
3. **Learn Continuously:** Keep asking follow-up questions without restarting the chat.

### **Why Road Guardian?**
- **Comprehensive:** Covers everything you need to know for the test.
- **Interactive:** Enjoy a conversational and user-friendly learning experience.
- **Accessible:** Learn at your own pace, anytime, anywhere.
""")

# Initialize session state for follow-up queries
if "queries" not in st.session_state:
    st.session_state["queries"] = []

# Input for user query
query = st.text_input('Enter your query', key="query_input", on_change=handle_submit)

if st.button('Submit'):
    handle_submit()
