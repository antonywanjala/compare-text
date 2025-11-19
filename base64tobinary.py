import os

def string_to_binary(s: str) -> str:
    return ''.join(format(byte, '08b') for byte in s.encode('utf-8'))

def file_to_binary(path: str) -> str:
    if not os.path.isfile(path):
        raise FileNotFoundError(f"File not found: {path}")
    with open(path, 'rb') as f:
        return ''.join(format(byte, '08b') for byte in f.read())

def main():
    print("Choose input type:")
    print("1) Convert a STRING to binary")
    print("2) Convert a FILE to binary")
    choice = input("Enter 1 or 2: ").strip()

    if choice == "1":
        text = input("Enter the string: ")
        result = string_to_binary(text)
    elif choice == "2":
        path = input("Enter file path: ").strip()
        result = file_to_binary(path)
    else:
        print("Invalid choice.")
        return

    save = input("Save output to file? (y/n): ").strip().lower()
    if save == "y":
        out_path = input("Enter output filename: ").strip()
        with open(out_path, "w") as f:
            f.write(result)
        print(f"Binary output saved to {out_path}")
    else:
        print("\nBinary output:")
        print(result)

if __name__ == "__main__":
    main()
