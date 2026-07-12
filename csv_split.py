import os
import sys
import csv
from typing import List, Callable, Optional
from tqdm import tqdm

# --- FIX FOR FIELD LIMIT ERROR ---
# Dynamically increase the CSV field size limit to the system maximum.
# This prevents crashes when reading massive blocks of text in a single cell.
max_int = sys.maxsize
while True:
    try:
        csv.field_size_limit(max_int)
        break
    except OverflowError:
        max_int = int(max_int / 10)
# ----------------------------------


def split_csv_by_size(
        file_path: str,
        max_file_size_mb: float,
        on_chunk_complete: Optional[Callable[[str], None]] = None
) -> List[str]:
    """
    Splits a CSV file into multiple parts based on a maximum file size constraint.
    Maintains column headers across all parts and tracks progress.

    :param file_path: Absolute path to the source CSV file.
    :param max_file_size_mb: Maximum allowed size for each split file in Megabytes.
    :param on_chunk_complete: A callback function that receives the absolute path
                              of each completed chunk *immediately* when it finishes.
    :return: A list of absolute file paths of all generated split files.
    """
    if not os.path.isabs(file_path):
        file_path = os.path.abspath(file_path)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file at {file_path} does not exist.")

    # Convert MB to Bytes
    max_bytes = max_file_size_mb * 1024 * 1024
    total_file_size = os.path.getsize(file_path)

    # Extract directory, filename, and extension to construct output paths
    dir_name = os.path.dirname(file_path)
    base_name, ext = os.path.splitext(os.path.basename(file_path))

    generated_files = []
    part_number = 1

    with open(file_path, 'r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)

        try:
            header = next(reader)
        except StopIteration:
            print("The source CSV file is empty.")
            return []

        header_line = ",".join(header) + "\n"
        header_bytes = len(header_line.encode('utf-8'))

        current_out_file = None
        current_writer = None
        current_file_bytes = 0
        current_filepath = ""

        def start_new_split_file():
            nonlocal current_out_file, current_writer, current_file_bytes, part_number, current_filepath

            # If a file is already open, close it and trigger the live log callback
            if current_out_file:
                current_out_file.close()
                if on_chunk_complete:
                    on_chunk_complete(current_filepath)

            # Construct new absolute path
            new_filename = f"{base_name}_part{part_number}{ext}"
            current_filepath = os.path.join(dir_name, new_filename)

            # Open and write header
            current_out_file = open(current_filepath, 'w', newline='', encoding='utf-8')
            writer = csv.writer(current_out_file)
            writer.writerow(header)

            generated_files.append(current_filepath)
            part_number += 1

            return writer, header_bytes

        # Start the first chunk
        current_writer, current_file_bytes = start_new_split_file()

        with tqdm(total=total_file_size, unit='B', unit_scale=True, unit_divisor=1024, desc="Splitting CSV") as pbar:
            pbar.update(header_bytes)

            for row in reader:
                row_line = ",".join(row) + "\n"
                row_bytes = len(row_line.encode('utf-8'))

                if current_file_bytes + row_bytes > max_bytes and current_file_bytes > header_bytes:
                    current_writer, current_file_bytes = start_new_split_file()

                current_writer.writerow(row)
                current_file_bytes += row_bytes
                pbar.update(row_bytes)

        # Clean up and trigger callback for the very last file chunk
        if current_out_file:
            current_out_file.close()
            if on_chunk_complete:
                on_chunk_complete(current_filepath)

    return generated_files


# --- Example Usage ---
if __name__ == "__main__":
    # Replace these paths with your actual system paths
    target_csv = r"Stopgap"
    output_log_file = r"split_files_log.txt"
    max_size_per_file_mb = 4.0

    # Clear the log file if it already exists so we start fresh
    if os.path.exists(output_log_file):
        os.remove(output_log_file)

    # Define our real-time logging function
    def log_chunk_live(filepath: str):
        # 1. Print it to the console immediately (using tqdm.write so it doesn't break the progress bar)
        tqdm.write(f"[Completed Chunk] -> {filepath}")

        # 2. Append it to the text log file instantly
        with open(output_log_file, 'a', encoding='utf-8') as log:
            log.write(filepath + "\n")

    try:
        print(f"Starting split process for '{os.path.basename(target_csv)}'...")
        print(f"Live log text file location: {output_log_file}\n")

        # Pass the callback function into the splitter
        resulting_paths = split_csv_by_size(
            target_csv,
            max_size_per_file_mb,
            on_chunk_complete=log_chunk_live
        )

        print(f"\nFinished! Total files generated: {len(resulting_paths)}")

    except FileNotFoundError as fnf_error:
        print(f"Error: {fnf_error}\nPlease double-check your file path.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
