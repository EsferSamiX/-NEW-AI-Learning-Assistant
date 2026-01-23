import streamlit as st

def show_error_card(message: str):
    st.markdown(
        f"""
        <div style="
            background-color: #7f1d1d;
            color: #fecaca;
            padding: 18px;
            border-radius: 12px;
            border: 1px solid #dc2626;
            font-size: 16px;
            font-weight: 500;
            margin: 10px 0px;
        ">
            ⚠️ <b>Error</b><br>
            {message}
        </div>
        """,
        unsafe_allow_html=True
    )
