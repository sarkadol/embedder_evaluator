import requests
import json

# Define the API endpoint and authorization token
url = "https://chat.ai.e-infra.cz/api/models"

# Read the entire content of a text file into a string
with open("api_key.txt", "r", encoding="utf-8") as file:
    API_KEY = file.read()

# Set up headers with authorization
headers = {
    "Authorization": f"Bearer {API_KEY}"
}

# Make the GET request
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    model_ids = [f'"{item["id"]}"' for item in data.get("data", [])]

    for model in model_ids:
        print(model)
else:
    print(f"Error: {response.status_code}, {response.text}")
