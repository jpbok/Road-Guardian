import streamlit as st

def render_about_us():
    """Render the About Us page."""
    st.title("About Us")
    st.write("""
    ### Project Scope
    Road Guardian is designed to help learner drivers and riders prepare for theory tests by providing an interactive learning platform.

    #### Objectives
    - Enhance understanding of driving and riding theory concepts.
    - Provide intuitive, on-demand learning tools.

    ### Data Sources
    This project uses official PDFs of theory books, including basic, final and riding.

    ### Features
    - **Interactive Q&A**: Users can submit queries and get relevant explanations.
    - **AI-Generated Summaries**: Intelligent summaries and multiple-choice questions generated by ChatGPT.
    """)

def render_methodology():
    """Render the Methodology page."""
    st.title("Methodology")
    st.write("""
    ### Implementation Overview
    The Road Guardian web application processes data through the following steps:

    1. **Document Parsing**: PDF files are read, split into chunks, and stored with relevant metadata.
    2. **Vector Embedding**: Chunks are embedded for quick retrieval using vector stores.
    3. **Query Handling**: User inputs are processed to find relevant matches.
    4. **LLM Interaction**: The selected content is sent to an LLM for summarization and question generation.

    ### Process Flow Diagrams
    Below are the process flow diagrams for the two main user types: Learner Driver and Learner Rider.
    """)

    # Display the flow diagram for learner drivers
    st.image("./assets/flow_learner_driver.png", caption="Process Flow for Learner Driver", use_column_width=True)
    st.write("""
    **Description**: This diagram illustrates the process flow for the Learner Driver use case. It includes parsing data from the Basic and Final Theory PDFs, embedding chunks, and processing user queries to generate relevant information and MCQs.
    """)

    # Display the flow diagram for learner riders
    st.image("./assets/flow_learner_rider.png", caption="Process Flow for Learner Rider", use_column_width=True)
    st.write("""
    **Description**: This diagram outlines the process flow for the Learner Rider use case. It showcases data parsing from the Basic and Riding Theory PDFs, embedding chunks, handling user inputs, and generating output from the LLM.
    """)


