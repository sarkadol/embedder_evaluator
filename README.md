# Project Overview
This project contains several scripts designed to evaluate the performance of different embedders by analyzing their results and generating evaluation metrics. The scripts read the results from JSON files, process the data, and output the evaluation results to CSV files.


Scripts:
- 1_contact_embedder.py: Queries the embedder API with a specific question and retrieves the top results.
- 2_embedder_testing.py: Evaluates the performance of the embedder by querying it with a set of questions and comparing the retrieved documents with the correct documents.
- 3_evaluate_response.py: Processes the results of the embedder evaluation and calculates various metrics such as accuracy and mean position score.

- print_results.py: Prints a summary of the accuracy for each embedder and language combination.
- utils.py: Contains utility functions used by the other scripts.
- contact_chatbot.py: for testing the connection
- contact_embedder.py: for testing the connection
- analyze_mdx_files.py: take a look at the documents that the embedders work with

## 1_generate_questions.py

This script is responsible for querying the embedder API with a specific question and retrieving the top results. It reads the URL from a text file based on the chosen embedder and sends an HTTP POST request to the embedder API.

Key Functions:


load_url(embedder): Reads the URL from a text file based on the chosen embedder.
query_embedder(question, top_k): Sends a POST request to the embedder API and retrieves the top results. 
## 2_embedder_generation.py
This script evaluates the performance of the embedder by querying it with a set of questions and comparing the retrieved documents with the correct documents. It reads the URL from a text file based on the chosen embedder and processes the results to generate evaluation metrics.

Key Functions:


load_url(embedder): Reads the URL from a text file based on the chosen embedder.
query_embedder(question, top_k): Sends a POST request to the embedder API and retrieves the top results.
evaluate_embedder(json_file, q, k, d, lang, output_file): Evaluates the embedder by querying it with a set of questions and comparing the results with the correct documents. 

## 3_evaluate_response.py
This script processes the results of the embedder evaluation and calculates various metrics such as accuracy and mean position score. It reads the results from a JSON file, processes the data, and outputs the evaluation results to a CSV file.

Key Functions:


evaluate_results(embedder, language): Processes the results of the embedder evaluation and calculates various metrics such as accuracy and mean position score.
print_results.py
This script aggregates the evaluation results from multiple CSV files and prints a summary of the accuracy for each embedder and language combination.

Key Functions:


Aggregates evaluation results from multiple CSV files.
Prints a summary of the accuracy for each embedder and language combination.
Usage
Run 1_contact_embedder.py: This script queries the embedder API with a specific question and retrieves the top results.
Run 2_embedder_testing.py: This script evaluates the performance of the embedder by querying it with a set of questions and comparing the retrieved documents with the correct documents.
Run 3_evaluate_response.py: This script processes the results of the embedder evaluation and calculates various metrics such as accuracy and mean position score.
Run print_results.py: This script aggregates the evaluation results from multiple CSV files and prints a summary of the accuracy for each embedder and language combination.
Make sure to configure the embedder and language parameters in each script as needed.