import os
from pathlib import Path
from PIL import Image
from pillow_heif import register_heif_opener

# Register HEIC opener with Pillow
register_heif_opener()


def convert_heic(input_path_str, output_format="JPEG"):
    """
    Converts a HEIC image to JPEG or GIF while maintaining color profiles.
    """
    input_path = Path(input_path_str)

    if not input_path.exists():
        print(f"Error: The file {input_path} does not exist.")
        return

    output_format = output_format.upper()
    if output_format not in ["JPEG", "GIF"]:
        print("Error: Unsupported format. Please choose 'JPEG' or 'GIF'.")
        return

    ext = ".jpg" if output_format == "JPEG" else ".gif"
    output_path = input_path.with_suffix(ext)

    try:
        with Image.open(input_path) as img:
            # Extract the original color profile and Exif metadata
            original_icc_profile = img.info.get('icc_profile')
            original_exif = img.info.get('exif')

            # Convert to RGB (Required for JPEG/GIF compatibility)
            rgb_img = img.convert("RGB")

            # Prepare save arguments dictionary
            save_kwargs = {}
            if original_icc_profile:
                save_kwargs['icc_profile'] = original_icc_profile
            if original_exif and output_format == "JPEG":
                save_kwargs['exif'] = original_exif

            # For JPEG, set quality to maximum to prevent compression artifacts
            if output_format == "JPEG":
                save_kwargs['quality'] = 100
                save_kwargs['subsampling'] = 0

            # Save to the target format, passing the color profile along
            rgb_img.save(output_path, output_format, **save_kwargs)

            print(f"Success! Converted '{input_path.name}' to '{output_path.name}' (Colors Maintained)")

    except Exception as e:
        print(f"An error occurred during conversion: {e}\n")


# --- Interactive Terminal Execution ---
if __name__ == "__main__":
    user_input = input("Enter absolute file path to a HEIC file here: ").strip()
    user_input = user_input.strip("'\"")

    if user_input:
        print("\n--- Starting Conversion ---")
        convert_heic(user_input, output_format="JPEG")
        convert_heic(user_input, output_format="GIF")
    else:
        print("No file path provided.")