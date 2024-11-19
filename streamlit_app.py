import streamlit as st
from app.ui import render_ui
from app.pages import render_about_us, render_methodology
from app.sidebar import sidebar
#
def main():
    sidebar()
    
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select Page", ["Main App", "About Us", "Methodology"])

    if page == "Main App":
        driver_metadata_paths = ["documents/chunks/driver_metadata.json"]
        rider_metadata_paths = ["documents/chunks/rider_metadata.json"]
        render_ui(driver_metadata_paths, rider_metadata_paths, None, None)
    elif page == "About Us":
        render_about_us()
    elif page == "Methodology":
        render_methodology()

if __name__ == "__main__":
    main()
