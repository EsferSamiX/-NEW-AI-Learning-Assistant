import streamlit as st

from services.educational_chatbot.rag_service import (
    build_vectorstore_from_pdf,
    ask_question_with_rag,
    get_context_text,
)

from services.educational_chatbot.citation_service import generate_citations
from services.educational_chatbot.question_generator import (
    generate_questions_from_context,
)

from services.educational_chatbot.evaluation_service import (
    evaluate_exam_answers,
)

from services.educational_chatbot.memory_service import (
    ConversationMemoryService,
)



# EDUCATIONAL CHATBOT UI


def render_educational_chatbot():

    st.subheader("📘 Educational Chatbot")

    
    # SESSION STATE
    
    if "vectorstore" not in st.session_state:
        st.session_state.vectorstore = None
        st.session_state.pdf_name = None

    if "chat_memory" not in st.session_state:
        st.session_state.chat_memory = ConversationMemoryService()

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "practice_questions" not in st.session_state:
        st.session_state.practice_questions = []

    if "practice_answers" not in st.session_state:
        st.session_state.practice_answers = {}

    if "practice_result" not in st.session_state:
        st.session_state.practice_result = None

    
    # PDF UPLOAD
    
    uploaded_pdf = st.file_uploader("Upload PDF", type=["pdf"])

    if uploaded_pdf:
        if (
            st.session_state.vectorstore is None
            or st.session_state.pdf_name != uploaded_pdf.name
        ):
            with st.spinner("Processing PDF..."):
                st.session_state.vectorstore = build_vectorstore_from_pdf(uploaded_pdf)
                st.session_state.pdf_name = uploaded_pdf.name

                st.session_state.chat_history.clear()
                st.session_state.chat_memory.clear()
                st.session_state.practice_questions = []
                st.session_state.practice_answers = {}
                st.session_state.practice_result = None

            st.success("PDF indexed successfully.")

    if st.session_state.vectorstore is None:
        st.info("Upload a PDF to begin.")
        return

    st.divider()

    
    # MODE
    
    mode = st.radio(
        "Choose Mode",
        ["Ask Question", "Practice Mode"],
        horizontal=True,
    )

    
    # ASK QUESTION MODE
    
    if mode == "Ask Question":

        
        # Render full chat history
        
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

                if msg.get("citations"):
                    st.markdown("**📚 Sources:**")
                    for c in msg["citations"]:
                        st.markdown(f"- {c}")


        # Chat input
        
        user_question = st.chat_input(
            "Ask a question about the uploaded PDF..."
        )

        if user_question:

            
            # USER MESSAGE (CRITICAL FIX)
            
            st.session_state.chat_history.append(
                {"role": "user", "content": user_question}
            )

            # MUST RENDER IMMEDIATELY
            with st.chat_message("user"):
                st.markdown(user_question)

            
            # ASSISTANT RESPONSE
        
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):

                    answer, docs = ask_question_with_rag(
                        vectorstore=st.session_state.vectorstore,
                        question=user_question,
                        memory_text=st.session_state.chat_memory.get_context(),
                    )

                    st.markdown(answer)

                    citations = []

                    if not answer.lower().startswith(
                        "i could not find this information"
                    ):
                        citations = generate_citations(docs)

                        if citations:
                            st.markdown("**📚 Sources:**")
                            for c in citations:
                                st.markdown(f"- {c}")

            
            # SAVE MEMORY (hidden)
            
            st.session_state.chat_memory.add_turn(
                user_question,
                answer,
            )

            
            # SAVE CHAT HISTORY
            
            st.session_state.chat_history.append(
                {
                    "role": "assistant",
                    "content": answer,
                    "citations": citations,
                }
            )

   
    # PRACTICE MODE — FULL EXAM
 
    else:

        st.markdown("### 🎓 Exam Practice Mode")

        
        # GENERATE QUESTIONS
       
        if not st.session_state.practice_questions:

            col1, col2 = st.columns(2)

            with col1:
                num_q = st.selectbox(
                    "Number of questions",
                    [1, 2, 3, 4, 5],
                )

            with col2:
                difficulty = st.selectbox(
                    "Difficulty",
                    ["easy", "medium", "hard"],
                )

            if st.button("✨ Generate Questions", type="primary"):

                if difficulty == "easy":
                    retrieval_query = "definitions and basic explanations"
                elif difficulty == "hard":
                    retrieval_query = (
                        "internal mechanisms, step by step reasoning, limitations"
                    )
                else:
                    retrieval_query = (
                        "process flow, component roles, working mechanism"
                    )

                context = get_context_text(
                    vectorstore=st.session_state.vectorstore,
                    query=retrieval_query,
                    top_k=8,
                )

                st.session_state.practice_questions = generate_questions_from_context(
                    context=context,
                    num_questions=num_q,
                    difficulty=difficulty,
                )

                st.session_state.practice_answers = {}
                st.session_state.practice_result = None
                st.rerun()

        
        # SHOW QUESTIONS
       
        if st.session_state.practice_questions:

            st.markdown("### 📝 Answer All Questions")

            for idx, q in enumerate(
                st.session_state.practice_questions, start=1
            ):
                st.markdown(f"**Question {idx}:** {q}")

                st.session_state.practice_answers[q] = st.text_area(
                    label=f"Answer {idx}",
                    key=f"ans_{idx}",
                    height=160,
                )

            if st.button("Submit Exam", type="primary"):

                answers_list = [
                    st.session_state.practice_answers.get(q, "")
                    for q in st.session_state.practice_questions
                ]

                reference_context = get_context_text(
                    vectorstore=st.session_state.vectorstore,
                    query="important concepts",
                    top_k=10,
                )

                with st.spinner("Evaluating your answers..."):
                    st.session_state.practice_result = evaluate_exam_answers(
                        questions=st.session_state.practice_questions,
                        student_answers=answers_list,
                        reference_context=reference_context,
                    )

                st.rerun()

        
        # FINAL RESULT
     
        if st.session_state.practice_result:

            st.divider()
            st.markdown("## 🧠 Final Evaluation")
            st.write(st.session_state.practice_result)

            if st.button("🔁 Start New Exam"):
                st.session_state.practice_questions = []
                st.session_state.practice_answers = {}
                st.session_state.practice_result = None
                st.rerun()
