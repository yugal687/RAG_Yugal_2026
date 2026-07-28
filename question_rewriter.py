from llm import generate_answer


def rewrite_question(
    question: str,
    history: list[dict],
) -> str:
    if not history:
        return question

    recent_history = history[-4:]

    conversation = "\n".join(
        f"{message['role'].capitalize()}: {message['content']}"
        for message in recent_history
    )

    prompt = f"""
Rewrite the latest user question as a complete standalone question.

Use the conversation only to resolve unclear references such as:
- he
- she
- they
- it
- that
- this event
- that person

Do not answer the question.
Do not add facts.
Return only the rewritten question.

Conversation:
{conversation}

Latest user question:
{question}

Standalone question:
""".strip()

    rewritten = generate_answer(
        prompt,
        max_new_tokens=60,
    ).strip()

    return rewritten if rewritten else question