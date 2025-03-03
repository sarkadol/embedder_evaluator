import requests
import json

# URL API
url = "https://embedbase-ol.dyn.cloud.e-infra.cz/v1/ceritsc-documentation/search"

# Hlavičky HTTP požadavku
headers = {
    "Content-Type": "application/json"
}
question = "What are the two main components needed to run the Omero application in Kubernetes?"
# Data požadavku
data = {
    "query": question,
    "top_k": 5
}

# Odeslání požadavku s ignorováním SSL certifikátu
response = requests.post(url, headers=headers, json=data, verify=False)

# Převod odpovědi na JSON
response_data = response.json()

# Strukturovaný výstup
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
    print(f"  - Data: {similarity.get('data', 'N/A')[:100]}...")  # Zkrátíme na 500 znaků

