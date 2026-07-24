from llm import generate_answer


def build_judge_prompt(
    question,
    expected_answer,
    generated_answer,
    retrieved_chunks
):
    """
    Build the evaluation prompt for the LLM judge.
    """

    context = ""

    for chunk in retrieved_chunks:
        context += chunk["text"] + "\n\n"

    prompt = f"""

        You are an objective evaluator for a Retrieval-Augmented Generation (RAG) system.

        Your job is to evaluate the generated answer fairly.

        Evaluation Rules:

        1. An answer is CORRECT if it conveys the same meaning as the expected answer.

        2.An answer is fully correct only if it includes all essential facts in the
        expected answer. If it contains only part of the expected answer, reduce the
        score and set correct to false when an essential fact is missing.

        3. Do NOT require the exact same wording.

        4. Extra correct information should NOT make an answer incorrect.

        5. Mark correct=false only if the answer is wrong, contradicts the expected answer, or misses the main point.

        6. An answer is GROUNDED if every important factual claim is supported by the retrieved context.

        7. If the answer adds unsupported facts that are not found in the retrieved context, grounded should be false.

        8. Score from 0 to 10:

        - 9-10 = Excellent

        - 7-8 = Mostly correct

        - 5-6 = Partially correct

        - 3-4 = Mostly incorrect

        - 0-2 = Completely incorrect

        Question:

        {question}

        Expected Answer:

        {expected_answer}

        Retrieved Context:

        {context}

        Generated Answer:

        {generated_answer}

        Return ONLY valid JSON in this exact format:

        {{

            "correct": true,

            "grounded": true,

            "score": 10,

            "reason": "One short sentence."
            The reason must be one short sentence.

        }}"""

    return prompt


def judge_answer(
    question,
    expected_answer,
    generated_answer,
    retrieved_chunks
):
    """
    Run the LLM judge.
    """

    prompt = build_judge_prompt(
        question,
        expected_answer,
        generated_answer,
        retrieved_chunks
    )

    response = generate_answer(prompt, max_new_tokens=192, return_json=True)

    return response