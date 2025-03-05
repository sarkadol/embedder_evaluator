#!/bin/bash

# Run the scripts sequentially
echo "Running 1_generate_questions.py..."
python3 1_generate_questions.py

echo "Running 2_embedder_generating.py..."
python3 2_embedder_generating.py

echo "Running 3_evaluate_response.py..."
python3 3_evaluate_response.py

echo "All scripts executed successfully!"
