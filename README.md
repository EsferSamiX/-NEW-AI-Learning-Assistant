
# 🧑‍💻 AI Learning Assistant
![Python](https://img.shields.io/badge/python-3.10-blue)
![Streamlit](https://img.shields.io/badge/streamlit-1.30-red)
![License](https://img.shields.io/badge/license-MIT-yellow)
![Version](https://img.shields.io/badge/version-1.0.0-green)
![Status](https://img.shields.io/badge/status-active-success)

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

### Tech Stack
- Embedding Model : all-MiniLM-L6-v2
- Deployment : Streamlit Cloud
- LLM Model Used : Llama 3.3 70B versatile
- Python 3.11




```bash
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
├── .streamlit/
│   ├── config.toml
│   ├── secrets.toml
│   └── secrets_example.toml
│
├── services/
│   ├── ai_essay_writer/
│   │   ├── __init__.py
│   │   └── essay_writer_service.py
│   │
│   ├── ai_text_summarization/
│   │   ├── __init__.py
│   │   └── text_summarization_service.py
│   │   └──summarization_utils.py
│   ├── educational_chatbot/
│   │   ├── __init__.py
│   │   └── rag_service.py
│   │   └──citaion_service.py
│   │   └──evaluation_service.py
│   │   └──question_generator.py
│   ├── exam_study_planner/
│   │   ├── __init__.py
│   │   └── planner_service.py
│   │   └── planner_utils.py
|   |   └── schedule_builder.py
|   |   └── topic_expander.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── groq_client.py
│   │   ├── prompt_templates.py
│   │   └── embeddings_service.py
│   │   └── cache_service.py
│       └──pdf_service.py
        └──vectorstore_service.py
│   └── __init__.py
│
├── UI/
│   ├── __init__.py
│   ├── navigation.py
│   ├── home_ui.py
│   ├── educational_chatbot_ui.py
│   ├── essay_writer_ui.py
│   ├── exam_study_planner_ui.py
│   └── text_summarization_ui.py
│
├── utils/
│   ├── constants.py
│   └── text_utils.py
|   └── planner_prifiles.py
|   └── ui_helpers.py
│
├── venv311/                     # Local virtual environment (not pushed to GitHub)
│
├── app.py
├── Dockerfile                 # Streamlit application entry point
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
├── LICENSE
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
