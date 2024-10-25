import streamlit as st
from app.ui import render_ui

# Define paths for metadata and images
driver_metadata_paths = ["documents/chunks/driver_metadata.json"]
rider_metadata_paths = ["documents/chunks/rider_metadata.json"]

# Render the UI
render_ui(driver_metadata_paths, rider_metadata_paths, None, None)
