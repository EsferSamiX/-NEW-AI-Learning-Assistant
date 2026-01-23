import streamlit as st
import pandas as pd
from datetime import date
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from services.exam_study_planner.planner_service import generate_study_plan



# Helper

def format_time(minutes: int) -> str:
    if minutes < 60:
        return f"{minutes} min"

    hours = minutes // 60
    remaining = minutes % 60

    if remaining == 0:
        return f"{hours} hour" if hours == 1 else f"{hours} hours"

    return f"{hours} hour {remaining} min"



# Convert plan 

def plan_to_dataframe(plan):
    rows = []

    for day in plan:
        date_str = day["date"].strftime("%Y-%m-%d")
        first_row = True

        for session in day["sessions"]:

            # time
            if "minutes" in session:
                time_value = format_time(session["minutes"])
            else:
                time_value = f"{session.get('hours', 0)} hour"

            rows.append(
                {
                    "Date": date_str if first_row else "",
                    "Chapter": session.get("topic", ""),
                    "Task": session.get("type", "")
                    .replace("_", " ")
                    .title(),
                    "Time": time_value,
                }
            )

            first_row = False

    return pd.DataFrame(rows)


# Create PDF

def generate_pdf(df: pd.DataFrame) -> bytes:
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    x_margin = 40
    y = height - 40

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(
        x_margin,
        y,
        "AI Learning Assistant — Personalized Study Plan",
    )
    y -= 30

    pdf.setFont("Helvetica", 9)

    for _, row in df.iterrows():

        line = (
            f"{row['Date']:<12} | "
            f"{row['Chapter']:<20} | "
            f"{row['Task']:<15} | "
            f"{row['Time']}"
        )

        if y < 50:
            pdf.showPage()
            pdf.setFont("Helvetica", 9)
            y = height - 40

        pdf.drawString(x_margin, y, line)
        y -= 14

    pdf.save()
    buffer.seek(0)
    return buffer.read()



# MAIN UI

def render_exam_study_planner():

    st.subheader("📆 Exam Study Planner")

    if "chapters" not in st.session_state:
        st.session_state.chapters = [""]

    
    # Inputs
    
    exam_date = st.date_input(
        "Exam Date",
        min_value=date.today(),
    )

    daily_hours = st.number_input(
        "Daily Available Study Time (hours)",
        min_value=1,
        max_value=12,
        value=3,
    )

    difficulty = st.radio(
        "Overall Difficulty Level",
        ["easy", "medium", "hard"],
        horizontal=True,
    )

    st.markdown("### 📘 Topics / Chapters")

    
    # Chapter Inputs
    
    for i, chapter in enumerate(st.session_state.chapters):

        col_text, col_gap, col_btn = st.columns([8, 0.3, 1])

        with col_text:
            st.session_state.chapters[i] = st.text_input(
                f"Chapter {i + 1}",
                value=chapter,
                key=f"chapter_{i}",
            )

        with col_btn:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🗑️", key=f"delete_{i}"):
                st.session_state.chapters.pop(i)
                st.rerun()

    col1, col2 = st.columns(2)

    with col1:
        if st.button("➕ Add another chapter"):
            st.session_state.chapters.append("")
            st.rerun()

    with col2:
        if st.button("🧹 Clear all"):
            st.session_state.chapters = [""]
            st.rerun()

    
    # Generate plan
    
    if st.button("🚀 Generate Study Plan"):

        if exam_date <= date.today():
            st.error("Exam date must be in the future.")
            return

        chapters = [
            c.strip()
            for c in st.session_state.chapters
            if c.strip()
        ]

        if not chapters:
            st.warning("Please enter at least one chapter.")
            return

        topics_text = "\n".join(
            f"{c} | {difficulty} | high"
            for c in chapters
        )

        with st.spinner("Building intelligent adaptive study plan..."):
            plan = generate_study_plan(
                exam_date=exam_date,
                daily_hours=daily_hours,
                topics_text=topics_text,
            )

        st.success("✅ Study plan generated successfully.")

    
        # Table
        
        df = plan_to_dataframe(plan)

        st.markdown("### 📊 Study Schedule")
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
        )

        
        # PDF
        
        pdf_bytes = generate_pdf(df)

        st.download_button(
            label="⬇️ Download Study Plan (PDF)",
            data=pdf_bytes,
            file_name="exam_study_plan.pdf",
            mime="application/pdf",
        )
