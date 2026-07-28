# def build_prompt(question, results):
#     """
#     Build a prompt for the LLM using retrieved chunks.
#     """

#     context = []

#     for i, match in enumerate(results["matches"], start=1):

#         metadata = match["metadata"]

#         context.append(
#             f"""
# Context {i}
# Source: {metadata['source']}
# Chunk: {metadata['chunk_number']}

# {metadata['text']}
# """
#         )

#     context_text = "\n" + ("-" * 80 + "\n").join(context)

#     prompt = f"""
# You are a helpful AI assistant.

# Answer the user's question ONLY using the retrieved context below.

# Rules:

# 1. If your internal knowledge conflicts with the retrieved context, always trust the retrieved context.

# 2. Do not make assumptions.

# 3. If the answer is not in the context, reply exactly:

#    "I don't have enough information to answer that."

# 4. If the answer is spread across multiple retrieved contexts, combine the information into a single answer.

# 5. If the retrieved contexts contain conflicting information, state that the retrieved information is conflicting instead of choosing one answer.

# 6. Keep the answer concise and factual.

# 7. Answer in 1 to 3 complete sentences.

#     For "Who is..." questions, explain:

#     - who the person is,

#     - their role,

#     - and why they are important,

#     using only the retrieved context.

# Retrieved Context
# =================
# {context_text}

# =================

# Question:
# {question}

# Answer:
# """

#     return prompt


def detect_question_type(question: str) -> str:
    question_lower = question.lower().strip()

    if question_lower.startswith("who"):
        return "who"
    if question_lower.startswith("when"):
        return "when"
    if question_lower.startswith("where"):
        return "where"
    if question_lower.startswith("why"):
        return "why"
    if question_lower.startswith("how"):
        return "how"
    if question_lower.startswith("what"):
        return "what"

    return "general"


def get_answer_instruction(question_type: str) -> str:
    instructions = {
        "who": (
            "Explain who the person is, their role, and why they are important."
        ),
        "when": (
            "Give the date or time period directly, followed by a brief explanation if available."
        ),
        "where": (
            "Give the location directly and briefly explain its relevance."
        ),
        "why": (
            "Explain the main reason or causes clearly using the retrieved context."
        ),
        "how": (
            "Explain the process or method in a clear sequence."
        ),
        "what": (
            "Give a direct definition or explanation of the subject."
        ),
        "general": (
            "Provide a direct and complete answer to the question."
        ),
    }

    return instructions[question_type]


def build_prompt(question: str, retrieved_chunks: list[dict]) -> str:
    question_type = detect_question_type(question)
    answer_instruction = get_answer_instruction(question_type)

    context_parts = []

    for index, chunk in enumerate(retrieved_chunks, start=1):
        text = chunk.get("text", "")
        context_parts.append(f"[Context {index}]\n{text}")

    context = "\n\n".join(context_parts)

    return f"""
You are a document-based question-answering assistant.

Use only the retrieved context below to answer the question.

Instructions:
- Answer only the user's question.
- Do not use outside knowledge.
- Do not invent missing information.
- Do not ask follow-up questions.
- Do not generate quizzes or unrelated text.
- Answer in 1 to 3 complete sentences.
- {answer_instruction}
- If the answer is not present in the context, reply exactly:
  I don't have enough information to answer that.
- Stop immediately after the answer.

Retrieved Context:
{context}

Question:
{question}

Answer:
""".strip()