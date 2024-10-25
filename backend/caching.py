import streamlit as st
from streamlit.runtime.caching.hashing import HashFuncsDict
from backend.parsing import File
import backend.chunking as chunking
import backend.embedding as embedding

def file_hash_func(file: File) -> str:
    return file.id

@st.cache_data(show_spinner=False)
def bootstrap_caching():
    file_hash_funcs: HashFuncsDict = {File: file_hash_func}
    chunking.chunk_file = st.cache_data(show_spinner=False, hash_funcs=file_hash_funcs)(chunking.chunk_file)
    embedding.embed_files = st.cache_data(show_spinner=False, hash_funcs=file_hash_funcs)(embedding.embed_files)
