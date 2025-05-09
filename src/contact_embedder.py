import requests
import json
from utils import *

#----------------------------------------------
embedder = 6  # Change this to 2 for embedder_2
# !! embedder 3 needs FI EDUROAM or VPN
top_k = 5
lang = "en" # cz or en
use_auth = False
#----------------------------------------------

# Load the URL from the text file
url = load_url(embedder)
print(f"Using embedder url: {url}\n")
#--------------------------------------------------------------------------------------------
#https://embedbase-ol.dyn.cloud.e-infra.cz/v1/ceritsc-documentation/search
# HTTP request headers
if(use_auth):
    with open("api_key.txt", "r", encoding="utf-8") as file:
        api_key = file.read().strip()
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
else:
    headers = {
        "Content-Type": "application/json"
    }
if lang == "cz":
    question = "Jaké jsou dvě hlavní součásti potřebné ke spuštění aplikace Omero v Kubernetes?"
else:
    question = "What are the two main components needed to run the Omero application in Kubernetes?"

#question = "Jak lze zkontrolovat existující namespaces v Rancher GUI?"

# Request data
data = {
    "query": question,
    "top_k": top_k,
    #"chunk_context": -1,
    # -1 = document
    # 0 = only one chunk
    # >0 = number of chunks around the found one
    "dataset_ids": ["test_1024"],

}


# Sending the request while ignoring the SSL certificate
response = requests.post(url, headers=headers, json=data, verify=False)

response_data = {}
# Converting the response to JSON
try:
    response_data = response.json()
except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")
    # Pretty print the full response
    print(f"Status Code: {response.status_code}")
    #print(f"Response Text: {response.text}")

if (True):  # see full api
    print("\n--- Full API Response ---")
    print(json.dumps(response_data, indent=4))
    # Count and print the number of returned documents
    num_docs = len(response_data.get("similarities", []))
    print(f"\nNumber of returned documents: {num_docs}")

else:  # structured
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
        print(f"  - Data length: {len(similarity.get('data', 'N/A'))}")
        print(f"  - Chunknumber: {similarity.get('chunknum', 'N/A')}")