import pandas as pd
import glob

# Get all evaluation CSV files
csv_files = glob.glob("embedder_*/evaluation_*.csv")

# Store accuracy results
accuracy_results = []

for file in csv_files:
    df = pd.read_csv(file)

    # Extract embedder and language from filename
    filename = file.replace("\\", "/")  # Normalize path for consistency
    parts = filename.split("/")[-1].split("_")
    language = parts[1] if len(parts) > 2 else "unknown"  # Handle cases like "evaluation_1.csv"
    embedder = parts[-1].split(".")[0]  # Extract embedder number

    # Calculate accuracy
    total_questions = len(df)
    correct_matches = df["correct_found"].sum()
    accuracy = correct_matches / total_questions if total_questions > 0 else 0

    accuracy_results.append((filename, accuracy, correct_matches, total_questions))

# Convert results to a DataFrame
accuracy_df = pd.DataFrame(accuracy_results, columns=["Filename", "Accuracy", "Correct Matches", "Total Questions"])

# Save to CSV
accuracy_df.to_csv("all_accuracy_results.csv", index=False)

# Determine max length for formatting
max_filename_length = max(len(item[0]) for item in accuracy_results)

# Print results with alignment
for filename, accuracy, correct_matches, total_questions in sorted(accuracy_results):
    print(f"{filename.ljust(max_filename_length)}: Accuracy: {accuracy:6.2%} ({correct_matches}/{total_questions})")

print("\nResults saved to 'all_accuracy_results.csv'.")
