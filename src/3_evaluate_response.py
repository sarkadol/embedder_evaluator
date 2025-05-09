import json
import pandas as pd
import os


# Function to evaluate embedder results
def evaluate_results(embedder, language, number):
    results_file = f"embedder_{embedder}/results_{language}_{embedder}_{number}.json"
    output_file = f"embedder_{embedder}/evaluation_{language}_{embedder}_{number}.csv"

    if not os.path.exists(results_file):
        raise FileNotFoundError(f"Error: The results file '{results_file}' does not exist.")

    with open(results_file, 'r', encoding='utf-8') as f:
        results = json.load(f)

    evaluations = []
    correct_matches = 0
    total_questions = len(results["evaluations"])
    position_scores = []
    total_retrieved_docs = 0

    for entry in results["evaluations"]:
        question = entry["question"]
        correct_document = entry["correct_document"]
        question_lang = entry.get("correct_language", "unknown")
        retrieved_docs = entry["retrieved_documents"]
        total_retrieved_docs = len(retrieved_docs)

        print("retr docs",len(retrieved_docs))

        retrieved_titles = [doc["metadata"].get("title", "") for doc in retrieved_docs if "metadata" in doc]
        retrieved_langs = [doc["metadata"].get("lang", "unknown") for doc in retrieved_docs if "metadata" in doc]
        num_czech = sum(1 for lang in retrieved_langs if lang == "cz")
        num_engl = sum(1 for lang in retrieved_langs if lang == "en")
        #if(num_engl==0):
        #    num_engl = 5-num_czech

        correct_found = correct_document in retrieved_titles
        position = retrieved_titles.index(correct_document) + 1 if correct_found else None

        if correct_found:
            correct_matches += 1
            position_scores.append(1 / position)  # Higher score for earlier positions
        else:
            position_scores.append(0)

        evaluations.append({
            "question": question,
            "correct_document": correct_document,
            "retrieved_documents": ", ".join(retrieved_titles),
            "position": position,
            "correct_found": correct_found,
            "question_lang": question_lang,
            "num_czech": num_czech,
            "num_engl": num_engl,
            "total_retrieved_docs":total_retrieved_docs
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
    print("running 3_evaluate_response.py")

    # ----------------------------------------------
    embedder = 8  # Select embedder
    #language = "czech"  # Choose "english" or "czech"
    #number = 1  # number of the generation response (version of question 1 or 2)
    # ----------------------------------------------

    #df = evaluate_results(embedder, language,number)
    #print(df.head())

    languages = ["english", "czech"]
    versions = [1, 2]

    for lang in languages:
        for version in versions:
            df = evaluate_results(embedder, lang, version)
            if df is not None:
                print(df.head())
