# ======================================================
# ESSAY PROMPT TEMPLATE
# ======================================================

ESSAY_PROMPT = """
You are an academic writing assistant.

------------------------------------------------------
TOPIC VALIDATION (MANDATORY)
------------------------------------------------------

Before writing anything, determine whether the topic
has a clear and meaningful academic interpretation.

If the topic:

- is random characters
- is meaningless text
- contains no recognizable subject
- cannot be interpreted as a topic, issue, idea, or concept

Then respond ONLY with this exact sentence:

"The topic you provided does not appear to have a clear or meaningful academic interpretation. Please provide a valid topic or subject so that an essay can be generated."

Do NOT write an essay in that case.

------------------------------------------------------
ESSAY INSTRUCTIONS (ONLY IF TOPIC IS VALID)
------------------------------------------------------

Topic:
{topic}

Tone:
{tone}

Target length:
Approximately {word_limit} words.

Required structure:

IF no outline is provided:
- Introduction
- Body paragraph 1
- Body paragraph 2
- Conclusion

IF an outline is provided:
- Introduction
- One paragraph per outline point
- Conclusion

Optional outline:
{outline}

------------------------------------------------------
IMPORTANT RULES
------------------------------------------------------

- Do NOT copy text from any source
- Do NOT fabricate citations
- Do NOT mention real authors or research papers
- Use original wording only
- Write in continuous academic paragraphs
- Do NOT include headings or bullet points
- Always complete the final sentence
- Slightly exceeding the word limit is allowed
  to ensure a complete conclusion

Return ONLY the essay text.
"""


SHORT_SUMMARY_PROMPT = """
You are an expert academic summarizer.

Create a concise, coherent summary of the text.

Rules:
- Use your own wording only.
- Do NOT copy sentences verbatim.
- Do NOT add external information.
- Do NOT fabricate facts.
- Preserve the original meaning.
- Write in paragraph form.
"""

BULLET_SUMMARY_PROMPT = """
You are an expert academic summarizer.

Summarize the text into clear numbered key insights.

Rules:
- Use 5–10 numbered points.
- Format strictly as:
  1. ...
  2. ...
  3. ...
- Each point must capture one core idea.
- Do NOT use bullet symbols (•, -, *).
- Do NOT copy sentences verbatim.
- Do NOT add external information.
- Do NOT fabricate facts.
- Keep each point concise and factual.
"""

FINAL_BULLET_MERGE_PROMPT = """
You are an expert academic summarizer.

Combine the numbered summaries below into one final numbered list.

Rules:
- Use numbered points only (1., 2., 3., ...)
- Merge duplicate ideas
- Preserve important technical details
- Do NOT convert to paragraph form
- Do NOT add new information
- Keep between 5–10 numbered points

Summaries:
\"\"\"
{summaries}
\"\"\"
"""



FINAL_PARAGRAPH_MERGE_PROMPT = """
You are an expert academic summarizer.

Combine the following partial summaries into one coherent short summary.

Rules:
- Remove redundancy
- Preserve key ideas
- Maintain logical paragraph flow
- Do NOT add new information

Summaries:
\"\"\"
{summaries}
\"\"\"
"""


# ======================================================
# EXAM EVALUATION PROMPTS
# ======================================================


SINGLE_QUESTION_EVALUATION_PROMPT = """
You are an academic examiner.

Evaluate the student's answer STRICTLY using the reference material.

--------------------------------------------------
QUESTION:
{question}

STUDENT ANSWER:
{student_answer}

REFERENCE MATERIAL:
\"\"\"
{reference_context}
\"\"\"

--------------------------------------------------
MARKING SCHEME (TOTAL = 10 MARKS)

- Conceptual correctness (4 marks)
- Coverage of key points (3 marks)
- Explanation clarity (2 marks)
- Terminology and structure (1 mark)

--------------------------------------------------
RULES:
- Do NOT invent information
- Do NOT evaluate beyond the reference
- Partial credit allowed
- If answer is empty or irrelevant → score 0
- Be concise and academic

--------------------------------------------------
RETURN OUTPUT EXACTLY IN THIS FORMAT:

Marks: X/10

Strengths:
- point
- point

Weaknesses:
- point
- point

Comment:
short paragraph
"""



FINAL_EXAM_EVALUATION_PROMPT = """
You are an academic examiner preparing the FINAL exam result.

IMPORTANT RULES:
- Evaluate ONLY the questions listed below
- Total questions: {num_questions}
- Each question carries exactly 10 marks
- Maximum score: {max_score}
- Do NOT create additional questions
- Do NOT say "No marks available"

--------------------------------------------------
INDIVIDUAL EVALUATIONS:
{combined_evaluations}
--------------------------------------------------

TASKS:
1. Extract marks for each question
2. Calculate accurate total score
3. Identify strong concepts
4. Identify weak concepts
5. Give clear improvement advice

--------------------------------------------------
RETURN OUTPUT STRICTLY IN THIS FORMAT:

Question-wise Marks:
- Question 1: X/10
- Question 2: X/10
(only list existing questions)

Total Score:
XX/{max_score}

Strength Areas:
- topic
- topic

Weak Areas:
- topic
- topic

Overall Feedback:
short academic paragraph
"""



# ======================================================
# QUESTION GENERATION PROMPTS
# ======================================================


QUESTION_DIFFICULTY_INSTRUCTIONS = {
    "easy": """
Generate BASIC-LEVEL questions.

Cognitive level:
- remembering
- understanding

Question style:
- Define ...
- What is ...
- Identify ...
- State the meaning of ...
- Explain in simple terms ...

Avoid deep analysis or multi-step reasoning.
""",

    "medium": """
Generate INTERMEDIATE-LEVEL questions.

Cognitive level:
- application
- explanation
- reasoning

Question style:
- How does ... work?
- Explain the process of ...
- Describe the role of ...
- Why is ... important?
- Explain relationships between components
- Compare concepts briefly

Avoid trivial definitions and avoid extreme depth.
""",

    "hard": """
Generate ADVANCED-LEVEL questions.

Cognitive level:
- analysis
- evaluation
- synthesis
- deep reasoning

Question style:
- Explain step-by-step mechanisms
- Analyze why a method is used
- Discuss limitations and assumptions
- Compare alternatives critically
- Explain internal working in detail
- Describe mathematical, logical, or conceptual derivation
- Explain cause–effect relationships

Questions must require deep conceptual understanding.
""",
}


QUESTION_GENERATION_PROMPT = """
You are a professional academic instructor.

Your task is to generate questions for students based ONLY
on the study material provided below.

The subject domain may be ANY of the following:
- science
- mathematics
- engineering
- artificial intelligence
- business
- accounting
- economics
- history
- religion
- philosophy
- medicine
- law
- general education

==========================
DIFFICULTY LEVEL
==========================

{difficulty_instruction}

==========================
IMPORTANT RULES
==========================

✔ Questions MUST be:
- technical OR concept-based
- directly grounded in the given content
- educational and meaningful

✘ Questions MUST NOT include:
- author names
- publication details
- conference names
- paper titles
- historical trivia
- unrelated facts
- content outside the given text

✘ Do NOT ask:
- who wrote
- where published
- when introduced
- name of researcher

==========================
CONTENT
==========================

\"\"\"
{context}
\"\"\"

==========================
OUTPUT FORMAT
==========================

- Return exactly {num_questions} questions
- Numbered list only
- No answers
- No explanations
- No extra text
- Each question must be complete and clear

Generate now.
"""


# ======================================================
# RAG PROMPTS
# ======================================================


RAG_ANSWER_PROMPT = """
You are an educational assistant.

Answer the user's question STRICTLY using the provided
document context.

If the answer is not present in the document, reply
with EXACTLY this sentence:

"I could not find this information in the document."

--------------------------------------------------
{memory_section}

DOCUMENT CONTEXT:
{document_context}

--------------------------------------------------
QUESTION:
{question}

ANSWER:
"""


PDF_QUESTION_GENERATION_PROMPT = """
You are an experienced teacher.

Using ONLY the content below, generate
{num_questions} academic questions.

Rules:
- Questions must be answerable from the content
- Do NOT include answers
- Do NOT include explanations
- Do NOT ask author, conference, or publication questions
- Questions must test understanding, not memorization
- Return numbered list only
- No markdown formatting

CONTENT:
\"\"\"
{context}
\"\"\"
"""



# ======================================================
# EXAM STUDY PLANNER — TOPIC EXPANSION PROMPT
# ======================================================

TOPIC_EXPANSION_PROMPT = """
You are a qualified academic instructor.

A student provided only ONE chapter name:

"{topic}"

You must infer appropriate subtopics based on difficulty level.

---------------------------------------
DIFFICULTY LEVEL: {difficulty_upper}
GUIDANCE:
{difficulty_hint}
---------------------------------------

SYLLABUS RULES:
- Easy   → basic understanding, minimal theory
- Medium → normal curriculum depth
- Hard   → detailed conceptual and analytical depth

---------------------------------------
OUTPUT REQUIREMENTS:
- Return 6–12 subtopics
- Each subtopic must be 3–6 words only
- Curriculum-appropriate
- No explanations
- No commentary
- No headings
- Output MUST be numbered list only

EXAMPLE FORMAT:
1. Subtopic name
2. Subtopic name
3. Subtopic name
"""
