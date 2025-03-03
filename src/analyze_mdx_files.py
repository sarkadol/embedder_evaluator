import os
from collections import Counter

# Define the directory to search
DATA_DIR = "../data"  # Change this if your files are in another folder

# Define the required header (modify as needed)
REQUIRED_HEADER = "---\ntitle: "  # Example MDX frontmatter starts with YAML metadata


def count_mdx_files_and_check_headers(directory, language=None):
    """ Recursively count .mdx files, check for required headers, and analyze titles."""
    mdx_count = 0
    missing_header_files = []
    titles = []

    # Walk through the directory tree
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".mdx") and (language is None or (language == "czech") == file.endswith(".cz.mdx")):
                mdx_count += 1
                file_path = os.path.join(root, file)

                # Read the first few lines of the file
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()

                        # Check if the required header is present
                        if REQUIRED_HEADER not in content:
                            missing_header_files.append(file_path)

                        # Extract title if present
                        if content.startswith("---\n"):
                            lines = content.split("\n")
                            for line in lines:
                                if line.startswith("title: "):
                                    titles.append(line.replace("title: ", "").strip())
                                    break
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

    title_counts = Counter(titles)
    duplicate_titles = {title: count for title, count in title_counts.items() if count > 1}

    return mdx_count, missing_header_files, duplicate_titles


def count_czech_and_english_files(directory):
    """ Count Czech (.cz.mdx) and English (.mdx) files separately. """
    czech_data = count_mdx_files_and_check_headers(directory, "czech")
    english_data = count_mdx_files_and_check_headers(directory, "english")
    return czech_data[0], english_data[0], czech_data[2], english_data[2]


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

    return {name: paths for name, paths in filenames.items() if len(paths) > 1}


def find_largest_mdx_file(directory):
    """ Find the largest .mdx file by character count. """
    largest_file, largest_size = None, 0

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
    total_files, missing_headers, duplicate_titles = count_mdx_files_and_check_headers(DATA_DIR)
    czech_files, english_files, duplicate_czech_titles, duplicate_english_titles = count_czech_and_english_files(DATA_DIR)
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

    if duplicate_czech_titles:
        print(f"\nDuplicate Czech titles found ({len(duplicate_czech_titles)}):")
        for title, count in duplicate_czech_titles.items():
            print(f"- '{title}' appears {count} times")
    else:
        print("All Czech titles are unique.\n")

    if duplicate_english_titles:
        print(f"\nDuplicate English titles found ({len(duplicate_english_titles)}):")
        for title, count in duplicate_english_titles.items():
            print(f"- '{title}' appears {count} times")
    else:
        print("All English titles are unique.\n")

    if largest_file:
        print(f"The largest .mdx file is: {largest_file} with {largest_size} characters.")
    else:
        print("No .mdx files found!")
