#contact_chatbot.py
from src.methods import *

if __name__ == "__main__":
    # Fetch available models
    models = get_available_models()

    if models:
        for model in models:
            print(model)

        selected_model = models[0]
        print(f"\nUsing model: {selected_model}")

        # Read content from .mdx files
        mdx_text = read_mdx_files()

        #if mdx_text:
         #   print(f"\nLoaded .mdx content:\n{mdx_text[:100]}...")  # Show only first 500 chars

        # Define user query
        user_question = "Summarize the content of the uploaded MDX file."

        # Combine file content with the question
        full_prompt = f"{mdx_text}\n\nNow, based on the above content, {user_question}"

        print(f"\nYou: {user_question}")

        # Send to chatbot
        ai_response = chat_with_model(selected_model, full_prompt)

        print(f"\nChatbot: {ai_response}")
    else:
        print("No models available.")
