# import json


# def load_results(file_path):
#     """
#     Load evaluation results from a JSON file.
#     """
#     with open(file_path, "r") as file:
#         return json.load(file)

# def main():

#     results = load_results("evaluation/results.json")

#     print("=" * 80)
#     print(f"Total Questions: {len(results)}")
#     print("=" * 80)

#     for i, result in enumerate(results, start=1):

#         print(f"\nEvaluation #{i}")
#         print("-" * 80)

#         print(f"Question:\n{result['question']}\n")

#         print(f"Expected Answer:\n{result['expected_answer']}\n")

#         print(f"Generated Answer:\n{result['generated_answer']}\n")

#         print("Retrieved Chunks:")

#         for chunk in result["retrieved_chunks"]:
#             print(f"  Source : {chunk['source']}")
#             print(f"  Chunk  : {chunk['chunk_number']}")
#             print(f"  Score  : {chunk['score']:.4f}")
#             print(f"  Text   : {chunk['text'][:150]}...")
#             print()

#         print("Judge Output:")
#         print(result["judge"])

#         print("=" * 80)


# if __name__ == "__main__":
#     main()


import json
from pathlib import Path


RESULTS_FILE = Path("results.json")


def parse_judge(judge_value):
    """
    Convert the judge response into a Python dictionary.
    Handles:
    - judge already stored as a dictionary
    - valid JSON strings
    - JSON strings missing a final closing brace
    """

    if isinstance(judge_value, dict):
        return judge_value

    if not isinstance(judge_value, str):
        return None

    cleaned = judge_value.strip()

    start = cleaned.find("{")
    end = cleaned.rfind("}")

    if start == -1:
        return None

    if end != -1 and end > start:
        cleaned = cleaned[start:end + 1]
    else:
        cleaned = cleaned[start:] + "}"

    try:
        return json.loads(cleaned)

    except json.JSONDecodeError:
        return None


def main():
    if not RESULTS_FILE.exists():
        print(f"Results file not found: {RESULTS_FILE}")
        return

    with open(RESULTS_FILE, "r", encoding="utf-8") as file:
        results = json.load(file)

    total = len(results)

    if total == 0:
        print("No evaluation results found.")
        return

    correct_count = 0
    grounded_count = 0
    valid_judge_count = 0
    total_score = 0
    failed_questions = []
    invalid_judges = []

    for result in results:
        judge = parse_judge(result.get("judge"))

        if judge is None:
            invalid_judges.append(result)
            continue

        valid_judge_count += 1

        correct = judge.get("correct", False)
        grounded = judge.get("grounded", False)
        score = judge.get("score", 0)

        if correct:
            correct_count += 1

        if grounded:
            grounded_count += 1

        if isinstance(score, (int, float)):
            total_score += score

        if not correct or not grounded:
            failed_questions.append(
                {
                    "question": result.get("question"),
                    "expected_answer": result.get("expected_answer"),
                    "generated_answer": result.get("generated_answer"),
                    "judge": judge
                }
            )

    accuracy = (
        correct_count / valid_judge_count * 100
        if valid_judge_count > 0
        else 0
    )

    groundedness = (
        grounded_count / valid_judge_count * 100
        if valid_judge_count > 0
        else 0
    )

    average_score = (
        total_score / valid_judge_count
        if valid_judge_count > 0
        else 0
    )

    print("=" * 60)
    print("RAG Evaluation Report")
    print("=" * 60)

    print(f"Total Questions       : {total}")
    print(f"Valid Judge Results   : {valid_judge_count}")
    print(f"Invalid Judge Results : {len(invalid_judges)}")
    print()

    print(f"Correct Answers       : {correct_count}")
    print(f"Incorrect Answers     : {valid_judge_count - correct_count}")
    print()

    print(f"Grounded Answers      : {grounded_count}")
    print(f"Ungrounded Answers    : {valid_judge_count - grounded_count}")
    print()

    print(f"Accuracy              : {accuracy:.2f}%")
    print(f"Groundedness          : {groundedness:.2f}%")
    print(f"Average Judge Score   : {average_score:.2f} / 10")

    print("=" * 60)

    if failed_questions:
        print("Failed Questions")
        print("=" * 60)

        for index, failure in enumerate(failed_questions, start=1):
            judge = failure["judge"]

            print(f"\n{index}. {failure['question']}")
            print(f"Expected  : {failure['expected_answer']}")
            print(f"Generated : {failure['generated_answer']}")
            print(f"Score     : {judge.get('score', 0)}")
            print(f"Reason    : {judge.get('reason', 'No reason provided.')}")
            print("-" * 60)

    else:
        print("All valid evaluations passed.")

    if invalid_judges:
        print("\n" + "=" * 60)
        print("Invalid Judge Outputs")
        print("=" * 60)

        for result in invalid_judges:
            print(f"\nQuestion: {result.get('question')}")
            print(f"Raw judge output: {result.get('judge')}")
            print("-" * 60)


if __name__ == "__main__":
    main()