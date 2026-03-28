import os
import time


def find_and_save_folders(root_path, search_string):
    # 1. User Inputs
    #root_path = input("Enter the absolute path of the parent folder: ").strip()

    if not os.path.isdir(root_path):
        print("Error: Invalid directory path.")
        return

    #search_string = input("Enter the folder name string to search for: ").strip()
    output_file = "found_folders_" + str(time.time()) + ".txt"

    print(f"Searching... results will be saved to {output_file}")

    found_paths = []

    # 2. Walk through directories
    for root, dirs, files in os.walk(root_path):
        for folder_name in dirs:
            # Match logic
            if search_string.lower() in folder_name.lower():
                # Clean the folder name (remove leading/trailing spaces or dots)
                cleaned_name = folder_name.strip()

                # Reconstruct path with the cleaned folder name
                full_path = os.path.join(root, cleaned_name)

                # Normalize and escape for Python (double backslashes)
                # .encode('unicode_escape') ensures all slashes are doubled
                escaped_path = full_path.encode('unicode_escape').decode('utf-8')

                found_paths.append(escaped_path)

    # 3. Write to TXT file
    with open(output_file, "w") as f:
        for path in found_paths:
            f.write(path + "\n")

    print(f"Done! Found {len(found_paths)} folders.")
    return found_paths

if __name__ == "__main__":
    find_and_save_folders()