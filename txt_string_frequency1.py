import os
import csv
from collections import Counter
from tqdm import tqdm


def search_strings_in_txt(super_folder, search_terms, output_csv="search_results.csv"):
    """
    Recursively searches for .txt files inside a super-folder and counts the frequency
    of given search terms per file. Exports results to a CSV.

    Parameters:
        super_folder (str): Path to the super-folder containing .txt files.
        search_terms (list): List of strings to search for.
        output_csv (str): Filename for the output CSV.

    Returns:
        str: Path to the output CSV.
    """

    results = []
    txt_files = []

    # Collect all .txt files
    for root, _, files in os.walk(super_folder):
        for file in files:
            if file.lower().endswith(".txt"):
                txt_files.append(os.path.join(root, file))

    # Process with progress bar
    for file_path in tqdm(txt_files, desc="Processing files", unit="file"):
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read().lower()
        except Exception as e:
            print(f"Skipping {file_path}, error: {e}")
            continue

        file_counts = Counter()
        for term in search_terms:
            count = text.count(term.lower())
            file_counts[term] = count

        results.append({"file": file_path, **file_counts})

    # Write results to CSV
    fieldnames = ["file"] + search_terms
    with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow(row)

    return os.path.abspath(output_csv)


# Example usage
if __name__ == "__main__":
    folder = "C:\\Users\\awanj\\GitHub\\disruptive_innovation\\responses"
    terms = "grantor, PI, grant, research".split(",")
    terms = [t.strip() for t in terms if t.strip()]

    output_path = search_strings_in_txt(folder, terms)
    print(f"Results saved to: {output_path}")
