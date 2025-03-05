import requests
import json
from src.methods import *


#----------------------------------------------
embedder = 1  # Change this to 2 for embedder_2
top_k = 5
#----------------------------------------------


# Load the URL from the text file
url = load_url(embedder)

# HTTP request headers
headers = {
    "Content-Type": "application/json"
}
question = "What are the two main components needed to run the Omero application in Kubernetes?"
# Request data
data = {
    "query": question,
    "top_k": top_k
}

# Sending the request while ignoring the SSL certificate
response = requests.post(url, headers=headers, json=data, verify=False)

# Converting the response to JSON
response_data = response.json()

if(True):
    # Pretty print the full response
    print("\n--- Full API Response ---")
    print(json.dumps(response_data, indent=4))
else:

    # Structured output
    print("\n--- API Response ---")
    print(f"Url: {url}")
    print(f"ID: {response_data.get('id', 'N/A')}")
    print(f"Created: {response_data.get('created', 'N/A')}")
    print(f"Dataset ID: {response_data.get('dataset_id', 'N/A')}")
    print(f"Query: {response_data.get('query', 'N/A')}")

    print("\n--- Similarities ---")
    for i, similarity in enumerate(response_data.get("similarities", []), start=1):
        print(f"\nResult {i}:")
        print(f"  - Score: {similarity.get('score', 'N/A'):.4f}")
        print(f"  - ID: {similarity.get('id', 'N/A')}")
        print(f"  - Data: {similarity.get('data', 'N/A')}...")  # Shortened to 100 characters
