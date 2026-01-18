import csv
import os
import sys
import time


def get_tokens_word_level(text):
    """
    Splits text by whitespace, preserving punctuation attached to words.
    Example: "Hello, -world!" -> ['Hello,', '-world!']
    """
    return text.split()


def get_tokens_char_level(text):
    """
    Splits text into a list of every single character.
    """
    return list(text)


def get_status(ngram_text):
    """
    Analyzes the n-gram to classify what kind of characters it contains.
    """
    check_text = ngram_text.replace(" ", "")

    if len(check_text) == 0:
        return "Whitespace/Empty"

    if check_text.isalpha():
        return "Alpha Only"
    elif check_text.isdigit():
        return "Numeric Only"
    elif check_text.isalnum():
        return "Alphanumeric"
    else:
        return "Contains Punctuation/Symbols"


def sanitize_for_excel(text):
    """
    Prevents Excel from interpreting text as a formula (which causes #NAME? errors).
    If text starts with =, +, -, or @, we prepend a single quote (').
    """
    # Excel triggers formulas on these characters
    triggers = ('=', '+', '-', '@')

    if text.startswith(triggers):
        # The single quote tells Excel "This is text, not a formula"
        return "'" + text

    return text


def main():
    print("--- N-Gram Extractor (Excel Safe) ---")

    # --- 1. Get User Input ---
    file_path = input("Enter the path to your .txt file: ").strip().replace('"', '')

    try:
        max_n_input = input("Enter the maximum n-gram length: ")
        max_n = int(max_n_input)
    except ValueError:
        print("Error: Please enter a valid whole number.")
        return

    print("\nSelect Mode:")
    print("1. Word Level (e.g., 'Hello, world!') - Punctuation stays attached.")
    print("2. Character Level (e.g., 'o, ', ' w') - Includes punctuation as characters.")
    mode = input("Enter 1 or 2: ").strip()

    if mode == '2':
        mode_name = "char"
        print("Selected: Character Level")
    else:
        mode_name = "word"
        print("Selected: Word Level")

    output_csv = f"ngrams_{mode_name}_raw_output_" + str(time.time()) + ".csv"

    # --- 2. Read File ---
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return

    raw_text = ""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_text = f.read()
    except UnicodeDecodeError:
        print("UTF-8 read failed. Trying Windows-1252...")
        try:
            with open(file_path, 'r', encoding='cp1252') as f:
                raw_text = f.read()
        except Exception as e:
            print(f"Error reading file with fallback encoding: {e}")
            return
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # Replace newlines with spaces so n-grams don't break the CSV row structure
    raw_text = raw_text.replace('\n', ' ').replace('\r', '')

    # --- 3. Tokenize ---
    if mode_name == "word":
        tokens = get_tokens_word_level(raw_text)
    else:
        tokens = get_tokens_char_level(raw_text)

    if not tokens:
        print("File contained no valid data.")
        return

    print(f"Processing {len(tokens)} items...")

    # --- 4. Write to CSV ---
    seen_ngrams = set()

    try:
        # utf-8-sig ensures Excel recognizes the encoding correctly
        with open(output_csv, 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.writer(csvfile)

            writer.writerow(["N-gram", "Number of Characters", "Number of Words", "Status"])

            for n in range(1, max_n + 1):
                # Create sliding window
                ngrams_tuples = zip(*[tokens[i:] for i in range(n)])

                for gram_tuple in ngrams_tuples:
                    if mode_name == "word":
                        gram_str = " ".join(gram_tuple)
                    else:
                        gram_str = "".join(gram_tuple)

                    if gram_str not in seen_ngrams:
                        num_chars = len(gram_str)
                        # Count words roughly by spaces
                        num_words = len(gram_str.split()) if gram_str.strip() else 0
                        status = get_status(gram_str)

                        # --- SANITIZE STEP ---
                        # We sanitize strictly for the CSV write operation.
                        # This prevents "- text" from becoming "#NAME?"
                        safe_gram_str = sanitize_for_excel(gram_str)

                        writer.writerow([safe_gram_str, num_chars, num_words, status])
                        seen_ngrams.add(gram_str)

        print(f"\nSuccess! Extracted {len(seen_ngrams)} unique n-grams.")
        print(f"File saved to: {os.path.abspath(output_csv)}")

    except IOError as e:
        print(f"Error writing CSV file: {e}")


if __name__ == "__main__":
    main()