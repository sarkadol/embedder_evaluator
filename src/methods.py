import os
import requests

# Define API endpoints
MODELS_URL = "https://chat.ai.e-infra.cz/api/models"
CHAT_URL = "https://chat.ai.e-infra.cz/api/chat/completions"

# Read API key from file
with open("api_key.txt", "r", encoding="utf-8") as file:
    API_KEY = file.read().strip()

# Set up headers with authorization
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def get_available_models():
    """Fetch available AI models."""
    response = requests.get(MODELS_URL, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return [item["id"] for item in data.get("data", [])]
    else:
        print(f"Error fetching models: {response.status_code}, {response.text}")
        return []

def read_mdx_files(directory="../data/27-2-2025_docs"):
    """Read all .mdx files from the specified directory and return their content."""
    mdx_content = ""
    if not os.path.exists(directory):
        print(f"Directory '{directory}' not found.")
        return ""

    for filename in os.listdir(directory):
        if filename.endswith(".mdx"):
            file_path = os.path.join(directory, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    mdx_content += f"\n### {filename} ###\n"  # Add filename as a section
                    mdx_content += file.read() + "\n"
            except Exception as e:
                print(f"Error reading {filename}: {e}")

    return mdx_content.strip()

def chat_with_model(model_id, prompt):
    """Send a message to the selected AI model."""
    payload = {
        "model": model_id,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    response = requests.post(CHAT_URL, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        return data["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code}, {response.text}"
