import json


def load_results(file_path):
    """
    Load evaluation results from a JSON file.
    """
    with open(file_path, "r") as file:
        return json.load(file)

def main():

    results = load_results("evaluation/results.json")

    print("=" * 80)
    print(f"Total Questions: {len(results)}")
    print("=" * 80)

    for i, result in enumerate(results, start=1):

        print(f"\nEvaluation #{i}")
        print("-" * 80)

        print(f"Question:\n{result['question']}\n")

        print(f"Expected Answer:\n{result['expected_answer']}\n")

        print(f"Generated Answer:\n{result['generated_answer']}\n")

        print("Retrieved Chunks:")

        for chunk in result["retrieved_chunks"]:
            print(f"  Source : {chunk['source']}")
            print(f"  Chunk  : {chunk['chunk_number']}")
            print(f"  Score  : {chunk['score']:.4f}")
            print(f"  Text   : {chunk['text'][:150]}...")
            print()

        print("Judge Output:")
        print(result["judge"])

        print("=" * 80)


if __name__ == "__main__":
    main()