import streamlit as st
from backend.document_processing import handle_query_submission

def render_ui(driver_metadata_paths, rider_metadata_paths, driver_image_folders, rider_image_folders):
    password = st.text_input("Please Enter Password to Start :", type="password")
    PASSWORD = "Tptest"

    if password == PASSWORD:
        st.success("Welcome! Let's get started.")
        st.markdown("### Road Guardian Instructions")
        st.markdown(
            "1. Choose your learning path: select either 'Learner Driver' or 'Learner Rider.'\n"
            "2. Enter a question related to driving or riding theory.\n"
            "3. Road Guardian will retrieve answers directly from official theory resources to help with your preparation.\n"
            "4. Test your knowledge with a follow-up multiple-choice question to reinforce learning.\n"
        )
        st.markdown("---")
        learner_type = st.radio("Choose learner type", options=["Learner Driver", "Learner Rider"])
        
        if learner_type == "Learner Driver":
            metadata_paths = driver_metadata_paths
            image_folders = driver_image_folders
        else:
            metadata_paths = rider_metadata_paths
            image_folders = rider_image_folders

        query = st.text_area("Enter your question")
        
        if st.button("Submit"):
            progress_bar = st.progress(0)
            with st.spinner("Processing your query, please wait..."):
                progress_bar.progress(10)
                #st.write("Step 1: Retrieving relevant information from theory books...")
                findings, llm_response, mcqs = handle_query_submission(query, metadata_paths, image_folders)
                progress_bar.progress(70)
                #st.write("Step 2: Generating response using AI...")
                progress_bar.progress(100)

            if findings:
                st.markdown("### Theory Book Matches")
                for i, finding in enumerate(findings):
                    with st.expander(f"Match {i + 1}: {finding.page_content[:100]}..."):
                        st.write(f"Content: {finding.page_content}")
                        st.write(f"Metadata: {finding.metadata}")

                st.markdown("### Using AI technology to address your query.")
                st.write(llm_response)
                st.markdown("### Test Me: Knowledge Retention")
                st.write(mcqs)
            else:
                st.write("No relevant data found in the theory books.")
    else:
        st.warning("Incorrect password. Please try again.")
