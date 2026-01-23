import streamlit as st
from services.ai_essay_writer.essay_service import generate_essay


def render_essay_writer():

    st.subheader("✍️ AI Essay Writer")

    topic = st.text_input("Essay Topic")

    word_limit = st.number_input(
        "Word Limit",
        100,
        3000,
        500,
        step=100,
    )

    tone = st.selectbox(
        "Tone",
        ["Academic", "Formal", "Neutral", "Creative"],
    )

    outline = st.text_area("Optional Outline")

    if st.button("Generate Essay", disabled=not topic):
        essay = generate_essay(
            topic=topic,
            word_limit=word_limit,
            tone=tone.lower(),
            outline=outline,
        )

        st.markdown("### 📄 Generated Essay")
        st.write(essay)
