import requests
import json
import re
import random
from pathlib import Path

# API URL
EMBEDDER_URL = "https://embedbase-ol.dyn.cloud.e-infra.cz/v1/ceritsc-documentation/search"

# Headers for the request
HEADERS = {"Content-Type": "application/json"}


# Function to extract title using regex
def extract_title(text: str) -> str:
    match = re.search(r'---\s*title:\s*(.*?)\s*---', text, re.MULTILINE)
    return match.group(1).strip() if match else None


# Function to query the embedder API
def query_embedder(question: str, top_k: int):
    data = {"query": question, "top_k": top_k}
    response = requests.post(EMBEDDER_URL, headers=HEADERS, json=data, verify=False)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, Response: {response.text}")
        return None


# Function to evaluate the embedder
def evaluate_embedder(json_file, q, k, d, lang, output_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        questions_mapping = json.load(f)

    results = []
    selected_docs = random.sample(list(questions_mapping.keys()), min(d, len(questions_mapping)))

    for doc_title in selected_docs:
        questions = random.sample(questions_mapping[doc_title], min(q, len(questions_mapping[doc_title])))

        for question in questions:
            response_data = query_embedder(question, k)
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
    # Parameters set in code instead of command-line arguments
    q = 6  # Number of questions per document
    k = 5  # Number of top retrieved documents
    d = 100  # Number of documents to test
    lang = "english"  # Language of the questions ("czech" or "english")
    output_file = "results.json"  # Output file for results

    json_file = "questions_mapping_czech.json" if lang == "czech" else "questions_mapping_english.json"
    evaluate_embedder(json_file, q, k, d, lang, output_file)
