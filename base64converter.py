import base64
import os

filepath = input("Input file path: ")

if not os.path.isfile(filepath):
    raise FileNotFoundError(f"File not found: {filepath}")

# Extract extension
_, ext = os.path.splitext(filepath)
ext = ext.lstrip(".")

# Read the target file in binary mode
with open(filepath, "rb") as f:
    file_bytes = f.read()

# Encode to base64
encoded = base64.b64encode(file_bytes).decode("utf-8")

# Define the output file path (appends .txt to original file name)
output_filepath = f"{filepath}_base64.txt"

# Write the base64 string to a new .txt file
with open(output_filepath, "w") as text_file:
    text_file.write(encoded)

print(f"Extension: {ext}")
print(f"Success! Base64 output saved to: {output_filepath}")
