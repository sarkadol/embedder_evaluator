# **Embedder Evaluation Framework**

This project evaluates different embedders by analyzing their results and generating evaluation metrics. 
The scripts query embedders, process the retrieved data, and output evaluation results to JSON and CSV files.

## **Project Structure**

### **1. Query and Generate Questions**
- **[`1_generate_questions.py`](1_generate_questions.py)**  
  Generates questions for evaluation by reading `.mdx` files and using an AI model to create relevant queries.  
  **Key Functions:**  
  - `load_api_key(filepath)`: Reads API key from a file.  
  - `get_available_models()`: Fetches available AI models.  
  - `read_mdx_files(directory, language, max_files)`: Reads `.mdx` files and extracts content.  
  - `generate_questions(model_id, text, num_questions, language)`: Generates questions from the text.  
  - `process_mdx_files(language, max_files, num_questions, model_id, number)`: Processes `.mdx` files and saves generated questions.  

### **2. Query Embedders and Evaluate Their Performance**
- **[`2_embedder_generating.py`](2_embedder_generating.py)**  
  Evaluates an embedder’s performance by querying it with generated questions and retrieving the top results.  
  **Key Functions:**  
  - `query_embedder(question, top_k, embedder_url)`: Queries the embedder API.  
  - `evaluate_embedder(json_file, q, k, d, lang, embedder, output_file)`: Evaluates embedder performance and saves results.  

### **3. Analyze and Score the Embedder’s Results**
- **[`3_evaluate_response.py`](3_evaluate_response.py)**  
  Processes the results of the embedder evaluation, calculates metrics (accuracy, mean position score), and saves them to a CSV file.  
  **Key Functions:**  
  - `evaluate_results(embedder, language, number)`: Computes evaluation metrics and saves results.  

### **4. Helper Scripts**
- **[`contact_embedder.py`](contact_embedder.py)**  
  Tests connectivity to the embedder API by sending a sample query and displaying the retrieved results.  
- **[`contact_chatbot.py`](contact_chatbot.py)**  
  Tests the chatbot API by retrieving available models and generating responses from `.mdx` file contents.  
- **[`analyze_mdx_files.py`](analyze_mdx_files.py)**  
  Analyzes `.mdx` files used in the evaluation, checking for missing headers, duplicate titles, and large files.  
- **[`utils.py`](utils.py)**  
  Contains utility functions, including loading API keys, fetching available models, reading `.mdx` files, and handling requests.  

## **How to Use**
1. **Generate Questions:**  
   Run `1_generate_questions.py` to create questions from `.mdx` files.  
2. **Test Embedders:**  
   Run `2_embedder_generating.py` to evaluate embedders by querying them with generated questions.  
3. **Evaluate Results:**  
   Run `3_evaluate_response.py` to calculate accuracy and other metrics.  
4. **Analyze Results:**  
   Use `print_results.py` (not included in the uploaded files) to summarize accuracy across embedders.  
5. **Verify API Connectivity:**  
   Run `contact_embedder.py` and `contact_chatbot.py` to check if the embedders and chatbot APIs are working correctly.  

## **Embedders**
The scripts support querying different embedders via API:  
1. **Embedder 1:** `https://embedbase-ol.dyn.cloud.e-infra.cz/v1/ceritsc-documentation/search`  
2. **Embedder 2:** `https://embedbase.dyn.cloud.e-infra.cz/v1/ceritsc-documentation/search`
3. **Embedder 3:** `https://embedbase-dev.dyn.cloud.e-infra.cz/v1/test/search`  
4. **... (Additional embedders can be configured in the scripts)**  

## **Requirements**
- Python 3.x  
- Required dependencies installed via `pip install -r requirements.txt`  
- API key stored in `api_key.txt`  
