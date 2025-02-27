#analyze_mdx_files.py
import os
from collections import Counter

# Define the directory to search
DATA_DIR = "../data"  # Change this if your files are in another folder

# Define the required header (modify as needed)
REQUIRED_HEADER = "---\ntitle: "  # Example MDX frontmatter starts with YAML metadata


def count_mdx_files_and_check_headers(directory):
    """ Recursively count .mdx files and check for a required header. """
    mdx_count = 0
    missing_header_files = []

    # Walk through the directory tree
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".mdx"):
                mdx_count += 1
                file_path = os.path.join(root, file)

                # Read the first few lines of the file
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        first_lines = f.read(100)  # Read first 100 characters

                        # Check if the required header is present
                        if REQUIRED_HEADER not in first_lines:
                            missing_header_files.append(file_path)

                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

    return mdx_count, missing_header_files


def count_czech_and_english_files(directory):
    """ Count Czech (.cz.mdx) and English (.mdx) files separately. """
    czech_count = 0
    english_count = 0

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".cz.mdx"):
                czech_count += 1
            elif file.endswith(".mdx") and not file.endswith(".cz.mdx"):
                english_count += 1

    return czech_count, english_count


def find_duplicate_mdx_filenames(directory):
    """ Find duplicate .mdx filenames and report their locations. """
    filenames = {}

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".mdx"):
                if file in filenames:
                    filenames[file].append(root)
                else:
                    filenames[file] = [root]

    duplicates = {name: paths for name, paths in filenames.items() if len(paths) > 1}

    return duplicates


def find_largest_mdx_file(directory):
    """ Find the largest .mdx file by character count. """
    largest_file = None
    largest_size = 0

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".mdx"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        size = len(content)
                        if size > largest_size:
                            largest_size = size
                            largest_file = file_path
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

    return largest_file, largest_size


if __name__ == "__main__":
    # Run the check
    total_files, missing_headers = count_mdx_files_and_check_headers(DATA_DIR)
    czech_files, english_files = count_czech_and_english_files(DATA_DIR)
    duplicate_mdx_files = find_duplicate_mdx_filenames(DATA_DIR)
    largest_file, largest_size = find_largest_mdx_file(DATA_DIR)

    # Print the results
    print(f"\nTotal .mdx files found: {total_files}")
    print(f"Czech files (.cz.mdx): {czech_files}")
    print(f"English files (.mdx): {english_files}")

    if missing_headers:
        print(f"Files missing the required header ({len(missing_headers)}):")
        for file in missing_headers:
            print(f"- {file}")
    else:
        print(f"All files contain the required header: {REQUIRED_HEADER}\n")

    if duplicate_mdx_files:
        print(f"Duplicate .mdx filenames found ({len(duplicate_mdx_files)}):")
        for file, locations in duplicate_mdx_files.items():
            print(f"- {file} found in:")
            for location in locations:
                print(f"  - {location}")
    else:
        print("No duplicate .mdx filenames found!\n")

    if largest_file:
        print(f"The largest .mdx file is: {largest_file} with {largest_size} characters.")
    else:
        print("No .mdx files found!")
