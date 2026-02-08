import urllib.request
import sys
import time
from collections import Counter


def find_anagrams_to_file(user_input, max_words=4, filename="anagrams.txt"):
    # --- 1. SETUP ---
    print(f"Downloading dictionary...")
    # Using a standard clean dictionary (Google's 10k most common words)
    url = "https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english-no-swears.txt"

    try:
        with urllib.request.urlopen(url) as response:
            words_list = response.read().decode('utf-8').splitlines()
    except Exception as e:
        print(f"Error downloading dictionary: {e}")
        return

    # --- 2. PRE-PROCESSING ---
    clean_target = "".join(filter(str.isalpha, user_input.lower()))
    target_count = Counter(clean_target)

    # Filter dictionary: Keep only words that can be built from the target letters
    candidates = []
    for word in words_list:
        word = word.lower()
        # Skip single letters except 'a' and 'i'
        if len(word) < 2 and word not in ['a', 'i']:
            continue

        word_count = Counter(word)
        # Check if word is a subset of target letters
        if all(word_count[c] <= target_count[c] for c in word_count):
            candidates.append(word)

    candidates.sort(key=len, reverse=True)
    total_candidates = len(candidates)

    if total_candidates == 0:
        print("No valid words found in dictionary for these letters.")
        return

    print(f"Starting Search ({total_candidates} root words)...")
    print(f"Results will be saved to: {filename}")
    print("-" * 60)

    # Open file for writing
    with open(filename, "w") as f:
        f.write(f"Anagrams for: {user_input}\n")
        f.write("=" * 30 + "\n")

        found_anagrams = set()
        match_count = 0

        # --- 3. RECURSIVE SOLVER ---
        def backtrack(path, current_pool):
            nonlocal match_count

            # Base Case: No letters left -> VALID ANAGRAM
            if sum(current_pool.values()) == 0:
                phrase = " ".join(path).title()
                if phrase not in found_anagrams:
                    found_anagrams.add(phrase)
                    match_count += 1

                    # Write to file immediately
                    f.write(f"{phrase}\n")
                    f.flush()  # Ensure it writes to disk now

                    # Clear progress line, print match to console
                    sys.stdout.write('\r\033[K')
                    print(f"✨ MATCH #{match_count}: {phrase}")
                return

            if len(path) >= max_words:
                return

            # Try next word
            for word in candidates:
                # Optimization: Skip if word is longer than remaining letters
                if len(word) > sum(current_pool.values()):
                    continue

                word_count = Counter(word)

                # Check if word fits in current_pool
                can_fit = True
                for char, count in word_count.items():
                    if current_pool[char] < count:
                        can_fit = False
                        break

                if can_fit:
                    new_pool = current_pool.copy()
                    new_pool.subtract(word_count)
                    backtrack(path + [word], new_pool)

        # --- 4. RUN SEARCH ---
        for i, root_word in enumerate(candidates):
            # Progress Bar Logic
            percent = 100 * ((i + 1) / float(total_candidates))
            bar_len = 30
            filled_len = int(bar_len * (i + 1) // total_candidates)
            bar = '█' * filled_len + '-' * (bar_len - filled_len)

            sys.stdout.write(f'\rSearching: |{bar}| {percent:.1f}%')
            sys.stdout.flush()

            # Prepare pool
            root_count = Counter(root_word)
            start_pool = target_count.copy()
            start_pool.subtract(root_count)

            backtrack([root_word], start_pool)

        sys.stdout.write('\n')
        f.write("=" * 30 + "\n")
        f.write(f"Total Found: {match_count}\n")

    print("-" * 60)
    print(f"Done! Found {match_count} anagrams.")
    print(f"Check '{filename}' for the full list.")


# --- RUN ---
user_phrase = input("\nEnter word or phrase: ")
find_anagrams_to_file(user_phrase)