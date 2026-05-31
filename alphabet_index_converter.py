import base64
import os
import time
import random
import json
from tqdm import tqdm


def get_char_value(char, char_map, allow_random=True):
    """
    Strictly uses preset mapped values. If a character is missing,
    it generates a random one (if allowed) and adds it to the map.
    Zero incumbent/default ASCII mappings exist here.
    """
    if char in char_map:
        return char_map[char]

    if allow_random:
        # Generate a purely random value for unmapped characters
        val = random.randint(1, 1000)
        char_map[char] = val
        return val
    else:
        # Strict preset mode without random generation fallback
        raise ValueError(f"Character '{char}' not found in preset mapping.")


def get_word_breakdown(word, char_map, allow_random):
    """
    Converts a single word into its custom/random value sum breakdown.
    """
    if not word:
        return "", 0

    indices = [get_char_value(char, char_map, allow_random) for char in word]
    calculation = "+".join(map(str, indices))
    word_total = sum(indices)

    return f"{calculation}={word_total}", word_total


def process_text_with_cumulative_logic(text, n, mode='w', char_map=None, allow_random=True):
    """
    Processes text into custom value breakdowns.
    Inserts a summation after every n units (words or characters).
    Tracks the ultimate cumulative sum of all n_val segments.
    """
    if char_map is None:
        char_map = {}

    items = text if mode == 'c' else text.split()
    if not items:
        return "", char_map

    final_output = []
    current_group_breakdowns = []
    current_group_totals = []
    segment_history_totals = []

    unit_label = "chars" if mode == 'c' else "words"

    for i, item in enumerate(tqdm(items, desc="Calculating Values", unit=unit_label), 1):
        breakdown_str, item_sum = get_word_breakdown(item, char_map, allow_random)

        current_group_breakdowns.append(f"({breakdown_str})")
        current_group_totals.append(item_sum)

        if i % n == 0 or i == len(items):
            group_text = " + ".join(current_group_breakdowns)

            n_sum_calc = "+".join(map(str, current_group_totals))
            n_total = sum(current_group_totals)

            segment_history_totals.append(n_total)

            ultimate_calc = "+".join(map(str, segment_history_totals))
            ultimate_total = sum(segment_history_totals)

            segment = (f"{group_text} = (n_val Breakdown: ({n_sum_calc})={n_total}) "
                       f"[Ultimate Sum: ({ultimate_calc})={ultimate_total}]")

            final_output.append(segment)

            current_group_breakdowns = []
            current_group_totals = []

    return " | ".join(final_output), char_map


def convert_to_values(file_name, char_map, allow_random, n_val=59999, mode='c'):
    """
    Handles the cumulative tracking logic natively.
    """
    if not file_name or not os.path.isfile(file_name):
        print(f"Error: File '{file_name}' not found.")
        return

    print("\n--- Cumulative Breakdown (Strictly Preset/Random) ---")
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            content = f.read()

        output, final_map = process_text_with_cumulative_logic(
            content, n=n_val, mode=mode, char_map=char_map, allow_random=allow_random
        )

        out_path = os.path.join(os.path.dirname(file_name),
                                f"ultimate_sum_{str(time.time())}_{os.path.basename(file_name)}")

        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(output)

        print(f"\nSuccess! Calculated result saved to: {out_path}")

        map_out_path = os.path.join(os.path.dirname(file_name), f"char_map_{str(time.time())}.json")
        with open(map_out_path, 'w', encoding='utf-8') as f:
            json.dump(final_map, f, indent=4)
        print(f"Final character mapping record saved to: {map_out_path}")

    except Exception as e:
        print(f"Error processing file: {e}")


def main():
    print("--- Base64 Encoder & Custom Value Mapper ---")
    filepath = input("Input file path: ").strip().replace('"', '').replace("'", "")

    if not os.path.isfile(filepath):
        print(f"File not found: {filepath}")
        return

    # Base64 Encoding
    _, ext = os.path.splitext(filepath)
    ext = ext.lstrip(".")

    with open(filepath, "rb") as f:
        file_bytes = f.read()

    encoded = base64.b64encode(file_bytes).decode("utf-8")
    output_filepath = f"{filepath}_base64.txt"

    with open(output_filepath, "w") as text_file:
        text_file.write(encoded)

    print(f"Extension: {ext}")
    print(f"Success! Base64 output saved to: {output_filepath}")

    # Configuration
    print("\n--- Mapping Configuration ---")
    print("1: Purely Random (All values generated on the fly)")
    print("2: Preset Only (Will crash if an unmapped character is found)")
    print("3: Preset + Random (Uses preset when available, generates random for missing characters)")

    choice = input("Select mapping logic (1/2/3): ").strip()

    char_map = {}
    allow_random = True

    if choice in ['2', '3']:
        custom_map_path = input(
            "Enter path to a JSON file with preset mapping (or press Enter to input manually): ").strip().replace('"',
                                                                                                                  '').replace(
            "'", "")

        if custom_map_path and os.path.isfile(custom_map_path):
            with open(custom_map_path, 'r', encoding='utf-8') as f:
                char_map = json.load(f)
            print(f"Loaded {len(char_map)} mappings from {custom_map_path}")
        else:
            print("Enter your mappings in 'char=value' format, separated by commas (e.g., A=1, B=2, +=99).")
            manual_map = input("Mapping: ")
            for pair in manual_map.split(','):
                if '=' in pair:
                    k, v = pair.split('=', 1)
                    try:
                        char_map[k.strip()] = int(v.strip())
                    except ValueError:
                        pass
            print(f"Registered {len(char_map)} manual mappings.")

        if choice == '2':
            allow_random = False
            print("Mode: Strict Preset Only.")
        else:
            print("Mode: Preset + Random Fallback.")
    else:
        print("Mode: Purely Random.")

    # Execution
    convert_to_values(file_name=output_filepath, char_map=char_map, allow_random=allow_random, n_val=59999, mode='c')


if __name__ == "__main__":
    main()
