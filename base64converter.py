import base64
import os

# <<< COPY AND PASTE YOUR FILE PATH HERE >>>
filepath = r"C:\path\to\your\file.ext"
# Example: filepath = r"/home/user/image.png"

if not os.path.isfile(filepath):
    raise FileNotFoundError(f"File not found: {filepath}")

# Extract extension
_, ext = os.path.splitext(filepath)
ext = ext.lstrip(".")

with open(filepath, "rb") as f:
    file_bytes = f.read()

encoded = base64.b64encode(file_bytes).decode("utf-8")

print(f"Extension: {ext}")
print("Base64 output:")
print(encoded)
