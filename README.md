# 🧑‍💻 AI Learning Assistant

An intelligent multi-module learning assistant built using **Streamlit + LLMs**, designed to support:

- 📚 Educational Q&A (RAG-based)
- 📝 AI Essay Writing
- 📄 PDF Summarization
- 🧪 Question Generation
- 🧠 Exam Answer Evaluation
- 📆 Adaptive Exam Study Planning

---

## 🚀 Features

### ✅ Educational Chatbot
- Retrieval-Augmented Generation (RAG)
- PDF-grounded answers only
- Page-level context referencing
- Conversation memory support

---

### ✅ AI Essay Writer
- Academic structure enforcement
- Automatic topic validation
- Optional outline support
- Plagiarism-safe generation
- Adjustable tone and length

---

### ✅ Text & PDF Summarization
- Short summary mode
- Bullet-point mode
- Chunk-based summarization
- Large-PDF support
- Token-safe processing

---

### ✅ Question Generator
- Easy / Medium / Hard difficulty levels
- Context-grounded questions only
- No hallucinated facts
- Supports technical and non-technical domains

---

### ✅ Answer Evaluation System
- Rubric-based academic grading
- Single-question evaluation
- Multi-question exam evaluation
- Strict reference-only marking

---

### ✅ Intelligent Exam Study Planner
- Difficulty-aware planning
- Minute-level scheduling
- 30-minute focus blocks
- Adaptive overload handling
- Automatic revision cycles
- Subtopic expansion using LLMs
---
Embedding Model : all-MiniLM-L6-v2
Deployment : Streamlit Cloud
LLM Model Used : Llama 3.3 70B versatile
---

## 🏗️ Architecture Overview

UI (Streamlit)
↓
Service Layer
↓
Prompt Templates
↓
LLM Client (Groq)
↓
Vector Store (FAISS)

## 🧩 Folder Structure

ai-learning-assistant/
│
├── services/ # Core intelligence modules
│├── ai_essay_writer/
│├── ai_text_summarization/
│├── educational_chatbot/
│├── exam_study_planner/
│├── evaluation/
│├── question_generation/
│├── rag/
│└── core/
│
├── utils/
│├── prompt_templates.py # ⭐ All LLM prompts
│├── constants.py
│└── text_utils.py
│
├── UI/ # Streamlit UI components
│
├── .streamlit/
│├── config.toml
│├── secrets.toml # ignored
│└── secrets_example.toml
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore



## 🔐 Environment Setup

### 1️⃣ Install dependencies

```bash
pip install -r requirements.txt

2️⃣ Configure API key

Create:
.streamlit/secrets.toml
GROQ_API_KEY="your_api_key_here"


3️⃣ Run application

streamlit run app.py
🧠 LLM Design Philosophy

All prompts are centralized

No prompt logic inside services

Strict reference grounding

No hallucinated citations

Educational safety first

🧪 Supported Models

Groq LLM API

Easily extensible to:

OpenAI

Claude

Mistral

Local LLMs here used Llama 3.3 70B versatile

👨‍💻 Author

Md Esfer Abdus Sami
2026
