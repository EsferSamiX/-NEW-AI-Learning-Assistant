import streamlit as st
from streamlit_option_menu import option_menu

from UI.home_ui import render_home
from UI.educational_chatbot_ui import render_educational_chatbot
from UI.exam_study_planner_ui import render_exam_study_planner
from UI.essay_writer_ui import render_essay_writer
from UI.text_summarization_ui import render_text_summarizer



# PAGE MAP

PAGES = {
    "Home": "home",
    "Educational Chatbot": "educational_chatbot",
    "Exam Study Planner": "exam_study_planner",
    "AI Essay Writer": "ai_essay_writer",
    "AI Text Summarization": "ai_text_summarization",
}

REVERSE_PAGES = {v: k for k, v in PAGES.items()}


def render_navigation():

    
    # 1. SESSION STATE INITIALIZATION
    
    if "page" not in st.session_state:
        url_page = st.query_params.get("page", "home")
        st.session_state.page = (
            url_page if url_page in REVERSE_PAGES else "home"
        )

    
    # 2. SIDEBAR CSS (FOOTER MOVED SLIGHTLY UP)
    
    st.markdown(
        """
        <style>
        section[data-testid="stSidebar"] {
            height: 100vh !important;
        }

        div[data-testid="stSidebarContent"] {
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            height: 100vh !important;
            padding-bottom: 12px;
        }

        .css-1d391kg {
            padding-top: 1rem;
        }

        .sidebar-footer {
            text-align: center;
            padding: 12px 10px;
            margin-bottom: 12px;
            color: #94a3b8;
            font-size: 0.85rem;
            border-top: 1px solid #1e293b;
            white-space: nowrap;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    
    # 3. SIDEBAR NAVIGATION
    
    with st.sidebar:
        with st.container():
            selected_label = option_menu(
                menu_title="AI Learning Assistant",
                options=list(PAGES.keys()),
                icons=["house", "book", "calendar-check", "pencil", "file-text"],
                menu_icon="laptop",
                default_index=list(PAGES.values()).index(
                    st.session_state.page
                ),
                key="navigation_menu",
                styles={
                    "container": {
                        "padding": "8px",
                        "background-color": "#0f172a"
                    },
                    "icon": {
                        "color": "#93c5fd",
                        "font-size": "20px"
                    },
                    "nav-link": {
                        "font-size": "17px",
                        "text-align": "left",
                        "margin": "6px 0px",
                        "padding": "12px",
                        "border-radius": "10px",
                        "color": "white",
                    },
                    "nav-link-selected": {
                        "background-color": "#2563eb",
                        "color": "white",
                        "font-weight": "600",
                    },
                },
            )

        st.markdown(
            """
            <div class="sidebar-footer">
                2026 Developed by <b>Md Esfer Abdus Sami</b>
            </div>
            """,
            unsafe_allow_html=True,
        )

    
    # 4. SYNC URL 
    
    selected_slug = PAGES[selected_label]

    if st.session_state.page != selected_slug:
        st.session_state.page = selected_slug
        st.query_params["page"] = selected_slug

    
    # 5. PAGE ROUTER
    
    page = st.session_state.page

    if page == "home":
        render_home()

    elif page == "educational_chatbot":
        render_educational_chatbot()

    elif page == "exam_study_planner":
        render_exam_study_planner()

    elif page == "ai_essay_writer":
        render_essay_writer()

    elif page == "ai_text_summarization":
        render_text_summarizer()

