import streamlit as st
from backend.document_processing import handle_query_submission, format_mcqs
from app.utility import check_password  # Import the password check function

def render_ui(driver_metadata_paths, rider_metadata_paths, driver_image_folders, rider_image_folders):
    # Display the main page content
    st.title("Welcome to the 🚗Road Guardian App")
    st.write("This is the main page where you can explore features and start using the app.")

    # Display the disclaimer in a collapsible expander
    with st.expander("IMPORTANT NOTICE: Please read before proceeding"):
        st.write("""
        This web application is developed as a proof-of-concept prototype. The information provided here is NOT
        intended for actual usage and should not be relied upon for making decisions, especially those related to 
        financial, legal, or healthcare matters.

        Furthermore, please be aware that the LLM may generate inaccurate or incorrect information. You assume 
        full responsibility for how you use any generated output. Always consult with qualified professionals 
        for accurate and personalized advice.
        """)

    # Check if the password is correct before continuing
    if not check_password():
        st.stop()

    st.success("Welcome to Road Guardian! Let's get started.")
    st.markdown("### Road Guardian Instructions")
    st.markdown(
        "1. **Select Your Learning Path**: Choose between Learner Driver or Learner Rider to tailor your experience.\n"
        "2. **Ask a Question**: Enter a driving or riding theory question to receive comprehensive answers.\n"
        "3. **Get Answers from Trusted Resources**: Road Guardian will pull accurate information directly from official theory resources to support your learning.\n"
        "4. **View Detailed Matches**: Expand the theory book matches to explore relevant text and images sourced from official materials.\n"
        "5. **Reinforce Your Knowledge**: Test yourself with follow-up multiple-choice questions to solidify your understanding.\n"
    )

    learner_type = st.radio("Choose learner type", options=["Learner Driver", "Learner Rider"])
    metadata_paths = driver_metadata_paths if learner_type == "Learner Driver" else rider_metadata_paths

    query = st.text_area("Enter your question")

    if st.button("Submit"):
        with st.spinner("Processing your query, please wait for one minute"):
            findings, llm_response, mcqs = handle_query_submission(query, metadata_paths)

            # Display retrieved findings
            if findings:
                st.markdown("### Theory Book Matches")
                for i, finding in enumerate(findings):
                    with st.expander(f"Match {i + 1}: {finding.page_content[:100]}..."):
                        st.write(f"Content: {finding.page_content}")
                        st.write(f"Metadata: {finding.metadata}")
                        if 'images' in finding.metadata and finding.metadata['images']:
                            for image_path in finding.metadata['images']:
                                st.image(image_path, caption=f"Page {finding.metadata['page']} Image")

                # Display LLM response
                st.markdown("### AI-Generated Response")
                st.write(llm_response)

                # Display formatted MCQs
                st.markdown("### Test Me: Knowledge Retention")
                formatted_mcqs = format_mcqs(mcqs)
                st.markdown(formatted_mcqs, unsafe_allow_html=True)
            else:
                st.write("No relevant data found in the theory books.")
