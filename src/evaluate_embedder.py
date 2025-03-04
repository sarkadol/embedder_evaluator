import json
import pandas as pd
import argparse


# Function to evaluate embedder results
def evaluate_results(results_file, output_file):
    with open(results_file, 'r', encoding='utf-8') as f:
        results = json.load(f)

    evaluations = []
    correct_matches = 0
    total_questions = len(results)
    position_scores = []

    for entry in results:
        question = entry["question"]
        correct_document = entry["correct_document"]
        retrieved_documents = [doc["title"] for doc in entry["retrieved_documents"]]

        correct_found = correct_document in retrieved_documents
        position = retrieved_documents.index(correct_document) + 1 if correct_found else None

        if correct_found:
            correct_matches += 1
            position_scores.append(1 / position)  # Higher score for earlier positions
        else:
            position_scores.append(0)

        evaluations.append({
            "question": question,
            "correct_document": correct_document,
            "retrieved_documents": ", ".join(retrieved_documents),
            "position": position,
            "correct_found": correct_found
        })

    accuracy = correct_matches / total_questions if total_questions > 0 else 0
    mean_position_score = sum(position_scores) / total_questions if total_questions > 0 else 0

    print(f"Accuracy: {accuracy:.2%} ({correct_matches}/{total_questions})")
    print(f"Mean Position Score: {mean_position_score:.4f}")

    df = pd.DataFrame(evaluations)
    df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"Evaluation results saved to {output_file}")

    return df


if __name__ == "__main__":
    # Argument parser
    parser = argparse.ArgumentParser(description="Evaluate embedder results.")
    parser.add_argument("--results_file", type=str, required=True, help="Path to the JSON file with retrieved results.")
    parser.add_argument("--output_file", type=str, required=True, help="Path to save the evaluation CSV file.")

    args = parser.parse_args()

    df = evaluate_results(args.results_file, args.output_file)
    print(df.head())
