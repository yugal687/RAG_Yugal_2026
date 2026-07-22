def build_prompt(question, results):
    """
    Build a prompt for the LLM using retrieved chunks.
    """

    context = []

    for i, match in enumerate(results["matches"], start=1):

        metadata = match["metadata"]

        context.append(
            f"""
Context {i}
Source: {metadata['source']}
Chunk: {metadata['chunk_number']}

{metadata['text']}
"""
        )

    context_text = "\n" + ("-" * 80 + "\n").join(context)

    prompt = f"""
You are a helpful AI assistant.

Answer the user's question ONLY using the retrieved context below.

Rules:

1. If your internal knowledge conflicts with the retrieved context, always trust the retrieved context.

2. Do not make assumptions.

3. If the answer is not in the context, reply exactly:

   "I don't have enough information to answer that."

4. If the answer is spread across multiple retrieved contexts, combine the information into a single answer.

5. If the retrieved contexts contain conflicting information, state that the retrieved information is conflicting instead of choosing one answer.

6. Keep the answer concise and factual.

Retrieved Context
=================
{context_text}

=================

Question:
{question}

Answer:
"""

    return prompt