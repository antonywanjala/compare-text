import csv
import os
import sys
from collections import defaultdict


def get_user_inputs():
    print("--- Settings ---")

    # 1. Choose Mode
    while True:
        print("Analyze by:")
        print("  [1] Words (FAST - finds repeated phrases like 'have an apple')")
        print("  [2] Characters (SLOW - finds exact substrings like 've an ap')")
        mode_input = input("Selection (1 or 2): ").strip()

        if mode_input == '1':
            mode = 'word'
            unit_name = "words"
            break
        elif mode_input == '2':
            mode = 'char'
            unit_name = "characters"
            break
        else:
            print("Invalid selection. Please type 1 or 2.")

    # 2. Minimum Length
    while True:
        try:
            val = input(f"Enter minimum length in {unit_name} (integer): ").strip()
            min_len = int(val)
            if min_len < 1:
                print("Must be at least 1.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")

    # 3. File Path
    while True:
        file_path = input("Enter path to .txt file: ").strip()
        # Remove quotes if dragged-and-dropped
        file_path = file_path.replace('"', '').replace("'", "")

        if os.path.isfile(file_path):
            break
        else:
            print(f"Error: File not found at {file_path}")

    return mode, min_len, file_path


def find_raw_duplicates(text, min_len, mode):
    results = {}

    # Prepare data based on mode
    if mode == 'word':
        # Split into list of words (removes extra whitespace automatically)
        data_source = text.split()
        max_len = len(data_source)
        print(f"\n1. Tokenized into {max_len} words. Scanning...")
    else:
        # Use raw string
        data_source = text
        max_len = len(data_source)
        print(f"\n1. Loaded {max_len} characters. Scanning...")

    current_len = min_len

    while True:
        # Safety break if length exceeds content
        if current_len > max_len:
            break

        substring_counts = defaultdict(int)

        # SLIDING WINDOW
        range_limit = max_len - current_len + 1

        for i in range(range_limit):
            if mode == 'word':
                # Create a tuple of words (hashable) so we can use it as a dict key
                chunk = tuple(data_source[i: i + current_len])
                substring_counts[chunk] += 1
            else:
                chunk = data_source[i: i + current_len]
                substring_counts[chunk] += 1

        # Check this length level for valid duplicates
        found_valid_duplicate_at_this_level = False

        for chunk, count in substring_counts.items():
            if count > 1:
                # Convert tuple back to string for storage if in word mode
                if mode == 'word':
                    clean_str = " ".join(chunk)
                else:
                    clean_str = chunk

                # --- NEW FILTER: Exclude strings that are just whitespace ---
                if not clean_str.strip():
                    continue
                # ------------------------------------------------------------

                # If we passed the filter, mark that we found something valid
                found_valid_duplicate_at_this_level = True
                results[clean_str] = count

        if not found_valid_duplicate_at_this_level:
            # Optimization: If no valid duplicates exist at length X, stop scanning.
            # (Note: Technically purely blank duplicates might exist, but we don't care about them)
            # We check if there were *any* matches (even ignored ones) to decide if we stop.
            # But safer is: if substring_counts was empty or all counts were 1, break.
            if not any(c > 1 for c in substring_counts.values()):
                break

        # Progress Indicator
        sys.stdout.write(f"\r   >> Scanning length {current_len} {mode}s... (Found {len(results)} valid candidates)")
        sys.stdout.flush()

        current_len += 1

    print("\n   >> Scan complete.")
    return results


def clean_duplicates(raw_data):
    """
    Removes nested duplicates (Russian Doll logic).
    """
    # Sort by length of the STRING, longest first
    sorted_candidates = sorted(raw_data.keys(), key=len, reverse=True)
    final_results = []
    total = len(sorted_candidates)

    if total == 0:
        return []

    print(f"2. Filtering {total} candidates to remove subsets...")

    for i, candidate in enumerate(sorted_candidates):

        # Progress %
        if i % 10 == 0 or i == total - 1:
            percent = (i / total) * 100
            sys.stdout.write(f"\r   >> Status: {int(percent)}% complete")
            sys.stdout.flush()

        is_nested = False

        # Check against already kept (longer) strings
        for kept_string, kept_count in final_results:
            if candidate in kept_string:
                is_nested = True
                break

        if not is_nested:
            final_results.append((candidate, raw_data[candidate]))

    print("\n   >> Cleanup complete.")
    return final_results


def write_csv(data):
    current_time = str(time.time())
    filename = "duplicate_analysis_" + current_time + ".csv"
    headers = ["String Length", "Occurrences", "Phrase/String"]

    try:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            # Row format: Length, Count, String
            rows = [(len(s), c, s) for s, c in data]
            writer.writerows(rows)

        # Get Absolute Path
        abs_path = os.path.abspath(filename)

        print("-" * 30)
        print(f"SUCCESS: Analysis Complete.")
        print(f"Found {len(data)} unique duplicate sequences (blanks excluded).")
        print(f"Output File: {abs_path}")
        print("-" * 30)

    except PermissionError:
        print(f"\nERROR: Could not write to '{filename}'. Is it open in Excel?")
    except Exception as e:
        print(f"\nERROR writing CSV: {e}")


if __name__ == "__main__":
    try:
        # 1. Inputs
        mode, min_len, txt_file = get_user_inputs()

        # Read file
        with open(txt_file, 'r', encoding='utf-8') as f:
            full_text = f.read()

        # 2. Scan
        raw_duplicates = find_raw_duplicates(full_text, min_len, mode)

        if not raw_duplicates:
            print("No duplicates found with current settings.")
            sys.exit()

        # 3. Clean
        clean_data = clean_duplicates(raw_duplicates)

        # 4. Save
        write_csv(clean_data)

    except KeyboardInterrupt:
        print("\nCancelled.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
