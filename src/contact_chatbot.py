#contact_chatbot.py
from src.methods import *
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chat with an AI model using MDX content.")
    parser.add_argument("--question", type=str, help="Custom question to ask the chatbot.")
    parser.add_argument("--model", type=str, help="Specify the AI model to use.")

    args = parser.parse_args()

    # Fetch available models
    models = get_available_models()
    print("Available models:\n",models)

    if not models:
        print("No models available.")
        exit(1)

    # Select model (default to the first available model if none is specified)
    selected_model = args.model if args.model in models else models[0]
    print(f"\nUsing model: {selected_model}")

    # Read content from .mdx files
    mdx_text = read_mdx_files()

    # Define user query from the command-line argument
    user_question = args.question if args.question else "What is the title of this?"

    # Combine file content with the question
    full_prompt = f"{mdx_text}\n\nNow, based on the above content, {user_question}"

    print(f"\nYou: {user_question}")

    # Send to chatbot
    ai_response = chat_with_model(selected_model, full_prompt)

    print(f"\nChatbot: {ai_response}")
