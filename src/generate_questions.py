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
MDX_DIRECTORY = "../data/docs"
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


def extract_title(content):
    """Extract title from MDX content."""
    if content.startswith("---\n"):
        lines = content.split("\n")
        for line in lines:
            if line.startswith("title: "):
                return line.replace("title: ", "").strip()
    return None


def read_english_mdx_files(directory):
    """Recursively read all English .mdx files and return their content indexed by title."""
    mdx_files = {}
    if not os.path.exists(directory):
        print(f"Directory '{directory}' not found.")
        return {}

    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".mdx") and not filename.endswith(".cz.mdx"):
                file_path = os.path.join(root, filename)
                try:
                    with open(file_path, "r", encoding="utf-8") as file:
                        content = file.read()
                        title = extract_title(content)
                        if title:
                            mdx_files[title] = content
                        else:
                            print(f"Warning: No title found in {filename}")
                except Exception as e:
                    print(f"Error reading {filename}: {e}")

    return mdx_files


def generate_questions(model_id, text, num_questions=5):
    """Generate a list of questions using the Chat API."""
    prompt = (f"Imagine that you are a user trying to find things in documentation. "
              f"Read the following content and generate {num_questions} relevant questions, "
              f"that can be answered by reading this text. "
              f"Write each question on a new line, nothing more. Do not number them, use just new lines. The text: \n\n{text}")

    payload = {
        "model": model_id,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    response = requests.post(CHAT_URL, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        questions = data["choices"][0]["message"]["content"].strip().split("\n")
        return [q.strip() for q in questions if q.strip()]
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

    for i, (title, content) in enumerate(mdx_data.items()):
        if i >= 1:  # Maximum files processed
            break
        print(f"Generating questions for: {title}")
        questions = generate_questions(selected_model, content, num_questions=5)
        questions_data[title] = questions

    with open(OUTPUT_JSON, "w", encoding="utf-8") as json_file:
        json.dump(questions_data, json_file, indent=4)

    print(f"Questions saved to {OUTPUT_JSON}")


if __name__ == "__main__":
    process_english_mdx_files()
