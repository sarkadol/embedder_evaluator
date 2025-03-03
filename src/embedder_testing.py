# embedder_testing

"""no. I want to make a new python script that:
1) will contact the embedder
2) send q questions from each document d
3) read the k retrieved documents - the similarity score, title
4) somehow save the results so in the end I will be able to say, what is the best (in terms of language, question topic or later the embedder type
parameters: q number of questions used, czech/english language, number of retrieved top k returned dosuments, d number of documents (keys in the json) to use

the title can be exctracted from the data using regex, e.g.
def extract_title(text: str) -> str:
    \"""Extracts the title from a structured text file.\"""
    match = re.search(r'^title:\s*(.+)', text, re.MULTILINE)
    return match.group(1).strip() if match else None

I have files questions_mapping_czech and questions_mapping_english."""

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
    match = re.search(r'^title:\s*(.+)', text, re.MULTILINE)
    return match.group(1).strip() if match else None


# Function to query the embedder API
def query_embedder(question: str, top_k: int):
    data = {"query": question, "top_k": top_k}
    response = requests.post(EMBEDDER_URL, headers=HEADERS, json=data, verify=False)
    return response.json() if response.status_code == 200 else None


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
            if not response_data:
                continue

            retrieved_docs = [
                {"score": similarity.get("score", "N/A"), "title": extract_title(similarity.get("data", ""))}
                for similarity in response_data.get("similarities", [])
            ]

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
    q = 3  # Number of questions per document
    k = 5  # Number of top retrieved documents
    d = 5  # Number of documents to test
    lang = "english"  # Language of the questions ("czech" or "english")
    output_file = "results.json"  # Output file for results

    json_file = "questions_mapping_czech.json" if lang == "czech" else "questions_mapping_english.json"
    evaluate_embedder(json_file, q, k, d, lang, output_file)
