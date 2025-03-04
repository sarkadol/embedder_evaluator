import requests
import json
import re
import random
import argparse
from pathlib import Path


# Function to extract title using regex
def extract_title(text: str) -> str:
    match = re.search(r'---\s*title:\s*(.*?)\s*---', text, re.MULTILINE)
    return match.group(1).strip() if match else None


# Function to query the embedder API
def query_embedder(embedder_url: str, question: str, top_k: int):
    headers = {"Content-Type": "application/json"}
    data = {"query": question, "top_k": top_k}

    response = requests.post(embedder_url, headers=headers, json=data, verify=False)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, Response: {response.text}")
        return None


# Function to evaluate the embedder
def evaluate_embedder(embedder_url, json_file, q, k, d, lang, output_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        questions_mapping = json.load(f)

    results = []
    selected_docs = random.sample(list(questions_mapping.keys()), min(d, len(questions_mapping)))

    for doc_title in selected_docs:
        questions = random.sample(questions_mapping[doc_title], min(q, len(questions_mapping[doc_title])))

        for question in questions:
            response_data = query_embedder(embedder_url, question, k)
            if not response_data or "similarities" not in response_data:
                print(f"No valid response for question: {question}")
                continue

            retrieved_docs = []
            for similarity in response_data.get("similarities", []):
                extracted_title = extract_title(similarity.get("data", ""))
                if extracted_title:
                    retrieved_docs.append({
                        "score": similarity.get("score", "N/A"),
                        "title": extracted_title,
                        "ID": similarity.get('id', 'N/A')
                    })
                else:
                    print(f"Warning: No title extracted from response data: {similarity.get('data', '')}")

            results.append({
                "question": question,
                "correct_document": doc_title,
                "retrieved_documents": retrieved_docs
            })

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

    print(f"Results saved to {output_file}")


if __name__ == "__main__":
    # Argument parser
    parser = argparse.ArgumentParser(description="Evaluate an embedder by querying an API with questions.")
    parser.add_argument("--embedder_url", type=str,
                        default="https://embedbase-ol.dyn.cloud.e-infra.cz/v1/ceritsc-documentation/search",
                        help="Embedder API URL.")
    parser.add_argument("--num_questions", type=int, default=1, help="Number of questions per document.")
    parser.add_argument("--top_k", type=int, default=1, help="Number of top retrieved documents.")
    parser.add_argument("--num_docs", type=int, default=1, help="Number of documents to test.")
    parser.add_argument("--language", type=str, default="english", choices=["english", "czech"],
                        help="Language of the questions.")
    parser.add_argument("--output_file", type=str, default="results.json",
                        help="Output file for storing evaluation results.")

    args = parser.parse_args()

    json_file = f"questions_mapping_{args.language}.json"
    evaluate_embedder(args.embedder_url, json_file, args.num_questions, args.top_k, args.num_docs, args.language,
                      args.output_file)
