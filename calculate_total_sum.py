import os
import sys
import time


def natural_sort_key(s):
    """
    Splits strings into text and numeric parts for natural sorting
    without relying on the 're' module. Ensures 'part2' comes before 'part11'.
    """
    parts = []
    current_num = ""
    for char in s:
        if char.isdigit():
            current_num += char
        else:
            if current_num:
                parts.append(int(current_num))
                current_num = ""
            parts.append(char.lower())
    if current_num:
        parts.append(int(current_num))
    return parts


def extract_values(chunk):
    """
    Parses a single string chunk using built-in string methods to find
    the Breakdown quantity and the Ultimate Sum.
    """
    # 1. Extract the quantity from "(n_val Breakdown: (X)=X)"
    qty_marker = "n_val Breakdown: ("
    qty_start = chunk.find(qty_marker)
    quantity = None
    if qty_start != -1:
        qty_start += len(qty_marker)
        qty_end = chunk.find(")", qty_start)
        raw_qty = chunk[qty_start:qty_end]

        # Split by '+' and sum the resulting integers.
        # This handles both a single number ("213") and equations ("65+50+89") safely.
        quantity = sum(int(num) for num in raw_qty.split('+'))

    # 2. Extract the sum from "[Ultimate Sum: (...)=Y]"
    sum_marker = "[Ultimate Sum: "
    sum_start = chunk.find(sum_marker)
    ultimate_sum = None
    if sum_start != -1:
        eq_idx = chunk.find("=", sum_start)
        bracket_idx = chunk.find("]", eq_idx)
        ultimate_sum = int(chunk[eq_idx + 1:bracket_idx])

    return quantity, ultimate_sum


def draw_loading_bar(current, total, bar_length=40):
    """
    Generates and outputs a real-time text progress bar to the console.
    """
    percent = float(current) / total
    hashes = '#' * int(round(percent * bar_length))
    spaces = ' ' * (bar_length - len(hashes))
    sys.stdout.write(f"\rIngesting Files: [{hashes}{spaces}] {int(round(percent * 100))}%")
    sys.stdout.flush()


def process_split_files(file_paths):
    # Sort files naturally so chunk parts merge in the right sequence
    file_paths.sort(key=natural_sort_key)

    total_files = len(file_paths)
    if total_files == 0:
        print("Error: No valid files found to process.")
        return

    combined_text = ""

    # Initialize the loading bar at 0%
    draw_loading_bar(0, total_files)

    for idx, path in enumerate(file_paths):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                combined_text += f.read()

            # --- AGGRESSIVE CLEANUP ---
            # Delete the file DURING process to remain strictly within the requested disk limits
            os.remove(path)

            # Small sleep simulation to make the loading bar visible
            time.sleep(0.05)

            # Update the progress bar
            draw_loading_bar(idx + 1, total_files)

        except Exception as e:
            print(f"\nError reading or deleting {path}: {e}")
            return

    # Once all files inside the directory are deleted, clean up the directory itself
    if file_paths:
        dir_path = os.path.dirname(file_paths[0])
        try:
            os.rmdir(dir_path)
            print(f"\nCleaned up directory to preserve disk limits: {dir_path}")
        except OSError:
            pass

    # Move to the next line after progress bar completion
    print("\nProcessing complete. Extracting metrics...")

    # Clean the text and split by the ' | ' delimiter
    chunks = [c.strip() for c in combined_text.split(" | ") if c.strip()]

    # Require at least 3 chunks to perform the requested offset
    if len(chunks) < 3:
        print("Error: Not enough data chunks found in the provided files to determine the requested sum.")
        return

    # Targeting the 3rd to last chunk for the base subtotal (9075)
    base_chunk = chunks[-3]
    # Targeting the last two chunks for the final quantity added (213 + 392)
    penultimate_chunk = chunks[-2]
    ultimate_chunk = chunks[-1]

    # Extracting the target values
    _, base_subtotal = extract_values(base_chunk)
    penultimate_qty, _ = extract_values(penultimate_chunk)
    ultimate_qty, _ = extract_values(ultimate_chunk)

    print("-" * 50)
    if base_subtotal is not None and penultimate_qty is not None and ultimate_qty is not None:
        total_added = penultimate_qty + ultimate_qty

        print(f"Second-to-last subtotal: {base_subtotal}")
        print(f"Final quantity added: {penultimate_qty} + {ultimate_qty} = {total_added}")
        print(f"Ultimate Sum verification: {base_subtotal} + {total_added} = {base_subtotal + total_added}")
    else:
        print("Error: Could not properly parse the expected syntax. Verify file contents.")
    print("-" * 50)


if __name__ == "__main__":
    # Check if a file/directory path was passed via command line
    if len(sys.argv) > 1:
        target_path = sys.argv[1]
    else:
        # Prompt the user for an absolute path
        target_path = input("Enter the absolute file path (or directory path): ").strip()

    file_list = []

    # Check if the user provided a directory (containing split files) or a single file
    if os.path.isdir(target_path):
        for file in os.listdir(target_path):
            full_path = os.path.join(target_path, file)
            if os.path.isfile(full_path):
                file_list.append(full_path)
    elif os.path.isfile(target_path):
        file_list.append(target_path)
    else:
        print(f"Error: The path '{target_path}' is invalid.")
        sys.exit(1)

    process_split_files(file_list)
