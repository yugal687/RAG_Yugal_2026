from pinecone_db import get_index
from retriever import retrieve
from prompt_builder import build_prompt
from llm import load_model, generate_answer


def main():

    print("Starting RAG Chatbot...")

    index = get_index()

    load_model()

    print("\nRAG Chatbot is ready!")
    print("Type 'exit' to quit.\n")

    while True:

        question = input("You: ")

        if question.lower() == "exit":
            break

        # Retrieve relevant chunks
        results = retrieve(index, question)

        # Build the prompt
        prompt = build_prompt(question, results)

        # Generate answer
        answer = generate_answer(prompt)

        print("\nAssistant:")
        print(answer)
        print()


if __name__ == "__main__":
    main()