import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("🚗 Road Guardian Chatbot")
st.write(
    "Welcome to the Road Guardian! This chatbot helps learner drivers prepare for their driving test by summarizing key driving theory points, offering test preparation tips, and highlighting areas for improvement. "
    "To use this app, you'll need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys)."
)

# Ask user for their OpenAI API key.
openai_api_key = st.text_input("Enter your OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Initialize session state for chat messages.
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "You are a chatbot that assists learner drivers by summarizing driving theory, providing test preparation tips, and explaining test results."}
        ]

    # Display chat history.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input for the chat.
    if prompt := st.chat_input("Ask your driving theory or test-related question here..."):
        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            stream=True,
        )

        # Stream and display the assistant's response.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})

# Possible future improvements:
# - Integration with a RAG model for real-time document retrieval from the theory book and test checklist.
# - Use chunking to break down complex driving theory topics for better understanding.
