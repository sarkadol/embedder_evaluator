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


def read_mdx_files(directory):
    """Read all .mdx files and return their content in a dictionary format."""
    mdx_files = {}
    if not os.path.exists(directory):
        print(f"Directory '{directory}' not found.")
        return {}

    for filename in os.listdir(directory):
        if filename.endswith(".mdx"):
            file_path = os.path.join(directory, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    mdx_files[filename] = file.read()
            except Exception as e:
                print(f"Error reading {filename}: {e}")

    return mdx_files


def generate_questions(model_id, text, num_questions=5):
    """Generate a list of questions using the Chat API."""
    prompt = f"Read the following content and generate {num_questions} relevant questions:\n\n{text}"

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


def process_mdx_files():
    """Read MDX files, generate questions, and save them in JSON format."""
    models = get_available_models()
    if not models:
        print("No available models.")
        return

    selected_model = models[0]
    mdx_data = read_mdx_files(MDX_DIRECTORY)

    questions_data = {}

    for filename, content in mdx_data.items():
        print(f"Generating questions for: {filename}")
        questions = generate_questions(selected_model, content, num_questions=5)
        questions_data[filename] = questions

    with open(OUTPUT_JSON, "w", encoding="utf-8") as json_file:
        json.dump(questions_data, json_file, indent=4)

    print(f"Questions saved to {OUTPUT_JSON}")


if __name__ == "__main__":
    process_mdx_files()
