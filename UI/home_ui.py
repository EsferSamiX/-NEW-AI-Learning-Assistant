import streamlit as st


def render_home():
    st.title("🧑‍💻 AI Learning Assistant")

    st.markdown(
        """
        ### Currently Offered Features:

        - 📘 Educational Chatbot (PDF-based Q&A)
        - 📆 Exam Study Planner with AI topic expansion
        - ✍️ AI Essay Writer
        - 📝 AI Text & PDF Summarization

        ---
        Designed for students, teachers, and self-learners.
        """
    )
