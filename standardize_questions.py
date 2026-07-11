import os
import time
import pandas as pd


def print_progress_bar(iteration, total, length=40):
    """Generates a dynamic text-based loading bar in the terminal."""
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = '█' * filled_length + '-' * (length - filled_length)

    # \r returns the cursor to the start of the line to overwrite the previous bar
    print(f'\rProcessing Files: |{bar}| {percent}% Complete', end='\r')

    # Print a new line when completed
    if iteration == total:
        print()


def merge_excel_prompts():
    # 1. Get user inputs interactively
    target_file = input("Enter the path to the target Excel file (arg1): ").strip().strip('"\'')
    source_folder = input("Enter the path to the super-folder (arg2): ").strip().strip('"\'')

    print("\nScanning folder for Excel files...")

    # 2. Load the target Excel file
    if not os.path.exists(target_file):
        print(f"Error: Target file '{target_file}' not found.")
        return

    try:
        target_df = pd.read_excel(target_file)
    except Exception as e:
        print(f"Error reading target file: {e}")
        return

    # Ensure required columns exist in the target file
    required_columns = ["ID", "Value", "Category", "Type1"]
    for col in required_columns:
        if col not in target_df.columns:
            target_df[col] = None

    if not os.path.isdir(source_folder):
        print(f"Error: Super-folder '{source_folder}' does not exist.")
        return

    # 3. First Pass: Gather all .xlsx files to get the total count for the loading bar
    excel_files = []
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            if file.endswith(".xlsx"):
                full_path = os.path.join(root, file)
                # Skip the target file if it's inside the source folder
                if os.path.abspath(full_path) != os.path.abspath(target_file):
                    excel_files.append(full_path)

    total_files = len(excel_files)
    if total_files == 0:
        print("No source Excel files found in the specified folder.")
        return

    all_prompts = []

    # Initialize the progress bar at 0%
    print_progress_bar(0, total_files)

    # 4. Second Pass: Read the files and update the loading bar
    for i, file_path in enumerate(excel_files):
        try:
            df = pd.read_excel(file_path)
            if 'Generated Prompt' in df.columns:
                prompts = df['Generated Prompt'].dropna().tolist()
                all_prompts.extend(prompts)
        except Exception as e:
            # Print warnings on a new line so it doesn't break the loading bar visually
            print(f"\nWarning: Could not read {os.path.basename(file_path)}. Error: {e}")

        # Update progress bar after each file
        print_progress_bar(i + 1, total_files)

    if not all_prompts:
        print("No 'Generated Prompt' data found in any of the source Excel files.")
        return

    print("\nFormatting and saving data to target file... please wait.")

    # 5. Create a DataFrame for the new rows
    new_rows = pd.DataFrame({
        "ID": [None] * len(all_prompts),
        "Value": all_prompts,
        "Category": ["Argument"] * len(all_prompts),
        "Type1": ["Node"] * len(all_prompts)
    })

    # 6. Append rows seamlessly starting from the first empty row
    updated_df = pd.concat([target_df, new_rows], ignore_index=True)

    # 7. Save to a NEW target file with an epoch timestamp to avoid permission errors
    try:
        epoch_time = int(time.time())
        # Split the base name and extension to insert the epoch before the .xlsx extension
        base_name, extension = os.path.splitext(target_file)
        new_target_file = f"{base_name}_{epoch_time}{extension}"

        updated_df.to_excel(new_target_file, index=False)
        print(f"Successfully added {len(all_prompts)} rows.")
        print(f"Resultant file saved as: '{new_target_file}'")
    except Exception as e:
        print(f"Error saving to new file: {e}")


if __name__ == "__main__":
    merge_excel_prompts()
