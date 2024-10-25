import streamlit as st

def sidebar():
    with st.sidebar:
        st.markdown("## Road Guardian Instructions")
        st.markdown(
            "1. Choose your learning path: select either 'Learner Driver' or 'Learner Rider.'\n"
            "2. Enter a question related to driving or riding theory.\n"
            "3. Road Guardian will retrieve answers directly from official theory resources to help with your preparation.\n"
            "4. Test your knowledge with a follow-up multiple-choice question to reinforce learning.\n"
        )
        st.markdown("---")

        st.markdown("# About")
        st.markdown(
            "Road Guardian is designed to support learner motorists in Singapore "
            "by providing answers to their questions, drawn directly from official theory documents."
        )
        st.markdown("This tool aims to simplify and enhance the learning journey for those preparing for their driving or riding tests.")
