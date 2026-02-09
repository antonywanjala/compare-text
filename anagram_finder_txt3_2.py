import time
import urllib.request
import sys
import os
from collections import Counter


def find_strict_anagrams_absolute_path(user_input, max_words=5, split_limit=29999):
    # --- 1. SETUP ---
    print("[1/3] Loading Strict Dictionary...")
    url = "https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english-no-swears.txt"

    try:
        with urllib.request.urlopen(url) as response:
            # Decode and clean lines
            raw_words = response.read().decode('utf-8').splitlines()
    except Exception as e:
        print(f"Error downloading dictionary: {e}")
        return

    # --- 2. PRE-PROCESSING & FILTERS ---
    # Clean input to pure letters
    clean_target = "".join(filter(str.isalpha, user_input.lower()))
    target_count = Counter(clean_target)

    # FILTER LOGIC:
    # 1. Remove words < 3 letters (Kill CA, NY, TX, Dr, St, etc.)
    # 2. exception: 'a' and 'i' are valid 1-letter words.
    # 3. Must be a subset of the input letters.
    candidates = []

    for word in raw_words:
        w = word.lower()
        if len(w) < 3 and w not in ['a', 'i']:
            continue

        w_count = Counter(w)
        if all(w_count[c] <= target_count[c] for c in w_count):
            candidates.append(w)

    # Sort longest first for better phrases
    candidates.sort(key=len, reverse=True)
    total_candidates = len(candidates)

    if total_candidates == 0:
        print("No valid words found in dictionary for these letters.")
        return

    # --- 3. FILE HANDLING ---
    created_files = []
    current_file_handle = None
    current_entries = 0
    file_index = 1

    def get_file_handle():
        nonlocal current_file_handle, current_entries, file_index

        # If no file open OR limit reached, rotate file
        if current_file_handle is None or current_entries >= split_limit:
            if current_file_handle:
                current_file_handle.close()

            # Create filename
            filename = f"strict_anagrams_part{file_index}_{str(time.time())}.txt"

            # GET ABSOLUTE PATH
            abs_path = os.path.abspath(filename)
            created_files.append(abs_path)

            # Open new file
            current_file_handle = open(filename, "w")
            current_file_handle.write(f"Strict Anagrams for: '{user_input}' (Part {file_index})\n")
            current_file_handle.write("=" * 60 + "\n")

            print(f"\n[System] Created: {os.path.basename(abs_path)}")
            file_index += 1
            current_entries = 0

        return current_file_handle

    # --- 4. RECURSIVE SOLVER ---
    print(f"[2/3] Searching {total_candidates} root words...")
    found_hashes = set()
    match_count = 0

    def backtrack(path, pool):
        nonlocal match_count, current_entries

        # Valid Anagram Found
        if sum(pool.values()) == 0:
            # Sort tuple to ensure uniqueness (ignoring word order)
            phrase_hash = tuple(sorted(path))

            if phrase_hash not in found_hashes:
                found_hashes.add(phrase_hash)
                match_count += 1
                current_entries += 1

                # Format string
                phrase_str = " ".join(path).title()

                # Write to file
                fh = get_file_handle()
                fh.write(phrase_str + "\n")

                # Console Feedback (periodically)
                if match_count % 50 == 0:
                    sys.stdout.write(f'\r✨ Found {match_count} phrases...')
                    sys.stdout.flush()
            return

        if len(path) >= max_words:
            return

        for word in candidates:
            # Optimization: Skip if word is longer than remaining letters
            if len(word) > sum(pool.values()): continue

            w_count = Counter(word)

            # Check if word fits in pool
            can_fit = True
            for char, count in w_count.items():
                if pool[char] < count:
                    can_fit = False
                    break

            if can_fit:
                new_pool = pool.copy()
                new_pool.subtract(w_count)
                backtrack(path + [word], new_pool)

    # --- 5. EXECUTION LOOP ---
    for i, root_word in enumerate(candidates):
        # Progress Bar
        percent = 100 * ((i + 1) / total_candidates)
        sys.stdout.write(f'\rProgress: {percent:.1f}% | Checking: {root_word}          ')
        sys.stdout.flush()

        root_count = Counter(root_word)
        start_pool = target_count.copy()
        start_pool.subtract(root_count)

        backtrack([root_word], start_pool)

    # Clean up
    if current_file_handle:
        current_file_handle.close()

    print("\n" + "=" * 60)
    print(f"SEARCH COMPLETE. Total Matches: {match_count}")
    print("Output saved to the following locations:")
    for fpath in created_files:
        print(f"📄 {fpath}")
    print("=" * 60)


# --- RUN ---
user_phrase = input("Enter phrase: ")
find_strict_anagrams_absolute_path(user_phrase)