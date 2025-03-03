import os
import json
import requests
import re

# Define API endpoints
MODELS_URL = "https://chat.ai.e-infra.cz/api/models"
CHAT_URL = "https://chat.ai.e-infra.cz/api/chat/completions"

# Read API key from file
def load_api_key(filepath="api_key.txt"):
    """Load API key from a file."""
    with open(filepath, "r", encoding="utf-8") as file:
        return file.read().strip()

API_KEY = load_api_key()

# Set up headers with authorization
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Directory containing MDX files
MDX_DIRECTORY = "../data/docs"
OUTPUT_JSON = "questions_mapping.json"


def get_available_models():
    """Fetch available AI models."""
    response = requests.get(MODELS_URL, headers=HEADERS)
    if response.status_code == 200:
        return [item["id"] for item in response.json().get("data", [])]
    print(f"Error fetching models: {response.status_code}, {response.text}")
    return []


def extract_title(text: str) -> str:
    """Extracts the title from a structured text file."""
    match = re.search(r'^title:\s*(.+)', text, re.MULTILINE)
    return match.group(1).strip() if match else None


def read_mdx_files(directory, language="english"):
    """Recursively read .mdx files of the chosen language and return their content indexed by title."""
    mdx_files = {}
    if not os.path.exists(directory):
        print(f"Directory '{directory}' not found.")
        return {}

    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".mdx") and (language == "czech") == filename.endswith(".cz.mdx"):
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


def generate_questions(model_id, text, num_questions=5, language="english"):
    """Generate a list of questions using the Chat API."""
    if language == "czech":
        prompt = (f"Představ si, že jsi uživatel, který se snaží najít informace v dokumentaci. "
                  f"Přečti si následující obsah a vygeneruj {num_questions} relevantních otázek, "
                  f"které lze zodpovědět na základě tohoto textu. "
                  f"Každou otázku napiš na nový řádek, nic víc. Nečísluj je, používej pouze nové řádky. Text: \n\n{text}")
    else:
        prompt = (f"Imagine that you are a user trying to find things in documentation. "
                  f"Read the following content and generate {num_questions} relevant questions, "
                  f"that can be answered by reading this text. "
                  f"Write each question on a new line, nothing more. Do not number them, use just new lines. The text: \n\n{text}")

    payload = {
        "model": model_id,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    response = requests.post(CHAT_URL, headers=HEADERS, json=payload)

    if response.status_code == 200:
        return [q.strip() for q in response.json()["choices"][0]["message"]["content"].strip().split("\n") if q.strip()]
    print(f"Error: {response.status_code}, {response.text}")
    return []


def process_mdx_files(language="english"):
    """Read MDX files in the chosen language, generate questions, and save them in JSON format."""
    models = get_available_models()
    if not models:
        print("No available models.")
        return

    selected_model = models[7]
    mdx_data = read_mdx_files(MDX_DIRECTORY, language)

    print(f"Processing {len(mdx_data)} {language} MDX files using model: {selected_model}")

    questions_data = {}
    for i, (title, content) in enumerate(mdx_data.items()):
        if i >= 70:  # Maximum files processed
            break
        print(f"Generating questions for: {title}")
        questions_data[title] = generate_questions(selected_model, content, num_questions=5, language=language)

    output_file = f"questions_mapping_{language}.json"
    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(questions_data, json_file, indent=4,ensure_ascii=False)
    print(f"Questions saved to {output_file}")


if __name__ == "__main__":
    #lang_choice = input("Choose language (english/czech): ").strip().lower()
    lang_choice = "czech"
    if lang_choice not in ["english", "czech"]:
        print("Invalid choice. Defaulting to English.")
        lang_choice = "english"
    process_mdx_files(lang_choice)
