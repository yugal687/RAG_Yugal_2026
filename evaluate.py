import json

from pinecone_db import get_index
from retriever import retrieve
from prompt_builder import build_prompt
from llm import load_model, generate_answer


def load_questions(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


def main():

    print("Loading model...")

    load_model()

    index = get_index()

    questions = load_questions("evaluation/evaluation_questions.json")

    results = []

    for item in questions:

        question = item["question"]

        expected = item["expected_answer"]

        retrieved = retrieve(index, question)

        prompt = build_prompt(question, retrieved)

        answer = generate_answer(prompt)

        retrieved_context = []

        for match in retrieved["matches"]:
            retrieved_context.append({
                "score": match["score"],
                "source": match["metadata"]["source"],
                "chunk_number": match["metadata"]["chunk_number"],
                "text": match["metadata"]["text"]
            })

        results.append({
            "question": question,
            "expected_answer": expected,
            "generated_answer": answer,
            "retrieved_chunks": retrieved_context
        })

        print(f"Finished: {question}")

    with open("evaluation/results.json", "w") as file:
        json.dump(results, file, indent=4)

    print("\nEvaluation Complete!")