import json

# Path to the JSON file containing the questions
QUESTIONS_JSON = "questions_mapping.json"


def load_questions():
    """Load questions from the JSON file."""
    try:
        with open(QUESTIONS_JSON, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: {QUESTIONS_JSON} not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from {QUESTIONS_JSON}.")
        return {}


def get_question(document_key, question_index):
    """Retrieve a specific question from the loaded JSON data."""
    questions_data = load_questions()

    if document_key not in questions_data:
        print(f"Error: Document '{document_key}' not found.")
        return None

    questions = questions_data[document_key]

    if question_index < 0 or question_index > len(questions):
        print(f"Error: Invalid question index {question_index}. Available range: 1-{len(questions)}")
        return None

    return questions[question_index]


if __name__ == "__main__":
    """Main function to prompt user for input and display the requested question."""
    document_key = "docs/news.mdx"
    question_index = 1

    question = get_question(document_key, question_index)

    if question:
        print(f"Question {question_index} from {document_key}: {question}")
