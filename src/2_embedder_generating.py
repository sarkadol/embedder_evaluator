import os
import requests
import json
import random
from pathlib import Path
from utils import *
import urllib3

#urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) # this supresses the unverified https request warning


# Function to query the embedder API
def query_embedder(question: str, top_k: int, embedder_url: str):
    data = {"query": question, "top_k": top_k}
    HEADERS = {"Content-Type": "application/json"}
    response = requests.post(embedder_url, headers=HEADERS, json=data, verify=False)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, Response: {response.text}")
        return None


# Function to evaluate the embedder
def evaluate_embedder(json_file, q, k, d, lang, embedder, output_file):
    embedder_url = load_url(embedder)

    with open(json_file, 'r', encoding='utf-8') as f:
        questions_mapping = json.load(f)

    results = {"embedder_url": embedder_url, "evaluations": []}
    selected_docs = random.sample(list(questions_mapping.keys()), min(d, len(questions_mapping)))

    for doc_title in selected_docs:
        doc_metadata = questions_mapping[doc_title]["metadata"]
        correct_lang = doc_metadata.get("lang", "unknown")
        questions = random.sample(questions_mapping[doc_title]["questions"], min(q, len(questions_mapping[doc_title]["questions"])))

        for question in questions:
            response_data = query_embedder(question, k, embedder_url)
            if not response_data or "similarities" not in response_data:
                print(f"No valid response for question: {question}")
                continue

            retrieved_docs = []
            for similarity in response_data.get("similarities", []):
                metadata = similarity.get("metadata", {})
                extracted_title = metadata.get("title")
                retrieved_lang = metadata.get("lang", "unknown")

                if extracted_title:
                    retrieved_docs.append({
                        "score": similarity.get("score", "N/A"),
                        "ID": similarity.get("id", "N/A"),
                        "metadata": {key: value for key, value in metadata.items() if key != "data"}
                    })
                else:
                    print(f"Warning: No title extracted from metadata: {metadata}")

            results["evaluations"].append({
                "question": question,
                "correct_document": doc_title,
                "correct_language": correct_lang,
                "retrieved_documents": retrieved_docs
            })

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

    print(f"Results saved to {output_file}")


if __name__ == "__main__":
    print("running 2_embedder_generating.py")
    # ----------------------------------------------
    q = 5  # Number of questions per document
    k = 5  # Number of top retrieved documents
    d = 100  # Number of documents to test
    lang = "english"  # Language of the questions ("czech" or "english")
    embedder = 6  # Change this to 2 for embedder_2

    number = 2 #number of the generation response !!! CHANGE THIS EVERY TIME !!!

    question_version = 2 # or 2
    # ----------------------------------------------

    output_file = f"embedder_{embedder}/results_{lang}_{embedder}_{number}.json"  # Output file for results

    json_file = f"questions_mapping_czech_{question_version}.json" if lang == "czech" else f"questions_mapping_english_{question_version}.json"

    # New addition here
    if os.path.exists(output_file):
        print(f"Output file '{output_file}' already exists.")
        user_input = input("Do you want to overwrite it? (yes/no): ").strip().lower()
        if user_input != "yes":
            print("Aborting process.")
            exit()

    evaluate_embedder(json_file, q, k, d, lang, embedder, output_file)
