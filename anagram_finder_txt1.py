import urllib.request
import sys
from collections import Counter


def find_anagrams_split_files(user_input, max_words=4, entries_per_file=29999):
    # --- 1. DICTIONARY SETUP ---
    print("Loading common English words...")
    url = "https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english-no-swears.txt"
    try:
        with urllib.request.urlopen(url) as response:
            words_list = response.read().decode('utf-8').splitlines()
    except Exception as e:
        print(f"Error: {e}")
        return

    # --- 2. PRE-PROCESSING ---
    clean_target = "".join(filter(str.isalpha, user_input.lower()))
    target_count = Counter(clean_target)

    candidates = []
    for word in words_list:
        word = word.lower()
        if len(word) < 2 and word not in ['a', 'i']: continue
        word_count = Counter(word)
        if all(word_count[c] <= target_count[c] for c in word_count):
            candidates.append(word)

    candidates.sort(key=len, reverse=True)
    total_candidates = len(candidates)

    if total_candidates == 0:
        print("No valid words found.")
        return

    # --- 3. STATE TRACKING ---
    found_anagrams = set()
    match_count = 0
    file_index = 1
    current_file_entries = 0
    current_file_handle = None

    def get_file_handle():
        nonlocal current_file_handle, file_index, current_file_entries
        if current_file_handle is None or current_file_entries >= entries_per_file:
            if current_file_handle:
                current_file_handle.close()

            filename = f"anagrams_part{file_index}.txt"
            current_file_handle = open(filename, "w")
            current_file_handle.write(f"Anagrams for: {user_input} (Part {file_index})\n")
            current_file_handle.write("=" * 40 + "\n")

            print(f"\n[System] Opening new file: {filename}")
            file_index += 1
            current_file_entries = 0
        return current_file_handle

    # --- 4. RECURSIVE SOLVER ---
    def backtrack(path, current_pool):
        nonlocal match_count, current_file_entries

        if sum(current_pool.values()) == 0:
            phrase = " ".join(path).title()
            if phrase not in found_anagrams:
                found_anagrams.add(phrase)
                match_count += 1
                current_file_entries += 1

                # Get the correct file handle (handles splitting logic)
                fh = get_file_handle()
                fh.write(f"{phrase}\n")

                # Feedback to console (every 100 matches to keep it fast)
                if match_count % 100 == 0:
                    sys.stdout.write(f'\r✨ Found {match_count} matches...')
                    sys.stdout.flush()
            return

        if len(path) >= max_words:
            return

        for word in candidates:
            if len(word) > sum(current_pool.values()): continue
            word_count = Counter(word)
            if all(current_pool[c] >= word_count[c] for c in word_count):
                new_pool = current_pool - word_count
                backtrack(path + [word], new_pool)

    # --- 5. EXECUTION ---
    print(f"Starting search. Splitting every {entries_per_file} entries.")

    for i, root_word in enumerate(candidates):
        # Console Progress Bar
        percent = 100 * ((i + 1) / total_candidates)
        bar = '█' * int(20 * (i + 1) // total_candidates) + '-' * (20 - int(20 * (i + 1) // total_candidates))
        sys.stdout.write(f'\rSearch Progress: |{bar}| {percent:.1f}%')
        sys.stdout.flush()

        root_count = Counter(root_word)
        backtrack([root_word], target_count - root_count)

    if current_file_handle:
        current_file_handle.close()

    print(f"\n\nSearch complete! Total entries: {match_count}")
    print(f"Files generated: {file_index - 1}")


# --- RUN ---
phrase = input("Enter phrase: ")
find_anagrams_split_files(phrase)