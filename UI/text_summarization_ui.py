import streamlit as st
from services.ai_text_summarization.summary_service import (
    summarize_text,
    summarize_pdf,
)


def render_text_summarizer():

    st.subheader("📝 AI Text Summarization")

    input_type = st.radio(
        "Input Type",
        ["Paste Text", "Upload PDF"],
    )

    mode = st.radio(
        "Summary Mode",
        ["Short Summary", "Bullet Key Points"],
    )

    mode_key = "bullet" if "Bullet" in mode else "short"

    if input_type == "Paste Text":
        text = st.text_area("Paste text here", height=250)

        if st.button("Generate Summary", disabled=not text):
            summary = summarize_text(text=text, mode=mode_key)
            st.write(summary)

    else:
        pdf = st.file_uploader("Upload PDF", type=["pdf"])

        if st.button("Generate Summary", disabled=pdf is None):
            summary = summarize_pdf(pdf_file=pdf, mode=mode_key)
            st.write(summary)
