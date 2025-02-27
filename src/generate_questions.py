import os
import json
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

# Directory containing MDX files
MDX_DIRECTORY = "../data/27-2-2025_docs"
OUTPUT_JSON = "questions_mapping.json"

def get_available_models():
    """Fetch available AI models."""
    response = requests.get(MODELS_URL, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return [item["id"] for item in data.get("data", [])]
    else:
        print(f"Error fetching models: {response.status_code}, {response.text}")
        return []

def read_english_mdx_files(directory):
    """Recursively read all English .mdx files and return their content in a dictionary format."""
    mdx_files = {}
    if not os.path.exists(directory):
        print(f"Directory '{directory}' not found.")
        return {}

    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".mdx") and not filename.endswith(".cz.mdx"):
                file_path = os.path.join(root, filename)
                key = f"{os.path.basename(root)}/{filename}"  # Use last folder and filename as key
                try:
                    with open(file_path, "r", encoding="utf-8") as file:
                        mdx_files[key] = file.read()
                except Exception as e:
                    print(f"Error reading {filename}: {e}")

    return mdx_files

def generate_questions(model_id, text, num_questions=5):
    """Generate a list of questions using the Chat API."""
    prompt = (f"Imagine that you are a user trying to find things in documentation."
              f"Read the following content and generate {num_questions} relevant questions, that can be answered by reading this text. "
              f"Write only questions, nothing more. The text: \n\n{text}")

    payload = {
        "model": model_id,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    response = requests.post(CHAT_URL, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        return data["choices"][0]["message"]["content"].split("\n")  # Split into individual questions
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return []

def process_english_mdx_files():
    """Read English MDX files, generate questions, and save them in JSON format."""
    models = get_available_models()
    if not models:
        print("No available models.")
        return

    selected_model = models[7]
    mdx_data = read_english_mdx_files(MDX_DIRECTORY)

    print(f"Processing {len(mdx_data)} English MDX files using model: {selected_model}")

    questions_data = {}

    for i, (key, content) in enumerate(mdx_data.items()):
        if i >= 10: # maximum files processed
            break
        print(f"Generating questions for: {key}")
        questions = generate_questions(selected_model, content, num_questions=5)
        questions_data[key] = questions

    with open(OUTPUT_JSON, "w", encoding="utf-8") as json_file:
        json.dump(questions_data, json_file, indent=4)

    print(f"Questions saved to {OUTPUT_JSON}")

if __name__ == "__main__":
    process_english_mdx_files()
