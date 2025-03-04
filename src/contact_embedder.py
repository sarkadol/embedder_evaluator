import requests
import json
import argparse


# Define function to send request to API
def search_query(api_url, question, top_k):
    """Send a search request to the specified API with a query and return top_k results."""
    headers = {"Content-Type": "application/json"}
    data = {"query": question, "top_k": top_k}

    try:
        response = requests.post(api_url, headers=headers, json=data, verify=False)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


if __name__ == "__main__":
    # Argument parser
    parser = argparse.ArgumentParser(description="Query an API for search results.")
    parser.add_argument("--question", type=str, required=True, help="The question to search for.")
    parser.add_argument("--top_k", type=int, default=5, help="Number of top results to return.")
    parser.add_argument("--api_url", type=str,
                        default="https://embedbase-ol.dyn.cloud.e-infra.cz/v1/ceritsc-documentation/search",
                        help="API endpoint URL.")

    args = parser.parse_args()

    # Execute search query
    response_data = search_query(args.api_url, args.question, args.top_k)

    if response_data:
        # Display response
        print("\n--- API Response ---")
        print(f"ID: {response_data.get('id', 'N/A')}")
        print(f"Created: {response_data.get('created', 'N/A')}")
        print(f"Dataset ID: {response_data.get('dataset_id', 'N/A')}")
        print(f"Query: {response_data.get('query', 'N/A')}")

        print("\n--- Similarities ---")
        for i, similarity in enumerate(response_data.get("similarities", []), start=1):
            print(f"\nResult {i}:")
            print(f"  - Score: {similarity.get('score', 'N/A'):.4f}")
            print(f"  - ID: {similarity.get('id', 'N/A')}")
            print(f"  - Data: {similarity.get('data', 'N/A')[:100]}...")  # Shortened to 100 characters
