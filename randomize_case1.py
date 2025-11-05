import random
import sys
# 1. Import the pyperclip library
# You may need to install it first: pip install pyperclip
try:
    import pyperclip
except ImportError:
    # Handle the case where pyperclip is not installed
    print("The 'pyperclip' library is required for clipboard functionality.")
    print("Please install it using: pip install pyperclip")
    sys.exit(1)


def randomize_case(input_string: str) -> str:
    """
    Produces a string with the same characters, but with random
    instances of capitalization and/or lower case status.

    Non-alphabetic characters (numbers, punctuation, spaces) remain unchanged.

    Args:
        input_string: The original string to process.

    Returns:
        The resultant string with randomized casing.
    """
    # Use a list comprehension for efficiency and readability
    randomized_chars = [
        # Check if the character is an alphabet
        # If it is alphabetic, randomly pick lower() or upper()
        char.lower() if random.choice([True, False]) else char.upper()
        if char.isalpha()
        # Otherwise, keep the character as is (e.g., spaces, numbers, punctuation)
        else char
        for char in input_string
    ]

    # Join the list of characters back into a single string
    return "".join(randomized_chars)


# --- Example Usage ---
if __name__ == "__main__":
    # Get input from command line arguments or use a default
    if len(sys.argv) > 1:
        # Join all arguments into a single string if the user provided multiple words
        initial_string = " ".join(sys.argv[1:])
    else:
        initial_string = input("Enter the string to randomize: ")
        print(f"--- Running with provided string: '{initial_string}' ---")

    # Generate the randomized string
    result_string = randomize_case(initial_string)

    # Print the results
    print("\nOriginal String:")
    print(f"  > {initial_string}")
    print("\nRandomized Case String:")
    print(f"  > {result_string}")

    # 2. Add the result string to the clipboard
    try:
        pyperclip.copy(result_string)
        print("\n✅ **Result copied to clipboard!** You can now press Ctrl+V to paste it.")
    except pyperclip.PyperclipException as e:
        print(f"\n⚠️ Could not copy to clipboard: {e}")
        print("Please ensure you have a clipboard tool installed (e.g., xclip or xsel on Linux).")


    # Run a few more times to demonstrate the randomness
    print("\nMore Examples:")
    for i in range(3):
        print(f"  Run {i + 1}: {randomize_case(initial_string)}")