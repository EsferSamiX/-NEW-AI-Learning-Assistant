

import hashlib
import streamlit as st


class CacheService:

    @staticmethod
    def generate_file_hash(file) -> str:

        file_bytes = file.getvalue()
        return hashlib.md5(file_bytes).hexdigest()

    @staticmethod
    def get_cached_vectorstore(file_hash: str):
        return st.session_state.get(f"vectorstore_{file_hash}")

    @staticmethod
    def set_cached_vectorstore(file_hash: str, vectorstore):
        st.session_state[f"vectorstore_{file_hash}"] = vectorstore

