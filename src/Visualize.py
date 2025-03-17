import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
file_path = "all_accuracy_results.csv"
df = pd.read_csv(file_path)

# Extract embedder names and evaluation types from the filename
df["Embedder"] = df["Filename"].apply(lambda x: x.split('/')[0])
df["Evaluation"] = df["Filename"].apply(lambda x: x.split('/')[1].replace(".csv", ""))

# Determine language from the filename
df["Language"] = df["Filename"].apply(lambda x: "Czech" if "czech" in x else ("English" if "english" in x else "Unknown"))

#------------------------------------------------

language_preference = "czech"  # Change this to "czech", "english", or "both"

#------------------------------------------------

# Apply filtering based on user preference
if language_preference == "czech":
    df = df[df["Language"] == "Czech"]
elif language_preference == "english":
    df = df[df["Language"] == "English"]

# Plot accuracy results
plt.figure(figsize=(12, 6))
bars = []
for embedder in df["Embedder"].unique():
    subset = df[df["Embedder"] == embedder]
    bars.extend(plt.bar(subset["Evaluation"], subset["Accuracy"], label=embedder))

# Add text labels on top of bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height, f"{height:.2%}", ha="center", va="bottom", fontsize=10)

plt.xlabel("Evaluation Files")
plt.ylabel("Accuracy")
plt.title(f"Accuracy Comparison ({language_preference.capitalize()})")
plt.xticks(rotation=45, ha="right")
plt.legend(title="Embedder")
plt.ylim(0.8, 1.0)  # Adjust the y-axis for better visualization
plt.grid(axis="y", linestyle="--", alpha=0.7)

# Show the plot
plt.tight_layout()
plt.show()
