import base64
import json
import os
import csv
from cryptography.fernet import Fernet

SAVE_JSON = "fernet_store.json"
SAVE_CSV = "fernet_output.csv"


def load_store():
    if os.path.exists(SAVE_JSON):
        with open(SAVE_JSON, "r") as f:
            return json.load(f)
    return {}


def save_store(store):
    with open(SAVE_JSON, "w") as f:
        json.dump(store, f, indent=4)


def append_csv(name, key, ciphertext):
    file_exists = os.path.exists(SAVE_CSV)

    with open(SAVE_CSV, "a", newline="") as f:
        writer = csv.writer(f)

        # header only included if new file
        if not file_exists:
            writer.writerow(["name", "key", "ciphertext"])

        writer.writerow([name, key, ciphertext])


def to_binary(data):
    if isinstance(data, bytes):
        return data
    return data.encode()


def encrypt_data(data, key=None):
    if key is None:
        key = Fernet.generate_key()
    f = Fernet(key)
    token = f.encrypt(data)
    return key, token


def main():
    store = load_store()
    print("\nFernet Encryption Utility (CSV Enabled)")
    print("--------------------------------------")

    while True:
        print("\nSelect an option:")
        print("1. Encrypt text")
        print("2. Encrypt binary (base64 input)")
        print("3. View saved JSON entries")
        print("4. Exit")

        choice = input("> ").strip()

        if choice == "1":
            text = input("Enter text to encrypt:\n> ")
            data = to_binary(text)
            key, token = encrypt_data(data)

            name = input("Name this entry (identifier):\n> ")
            key_str = key.decode()
            token_str = token.decode()

            store[name] = {"key": key_str, "ciphertext": token_str}
            save_store(store)
            append_csv(name, key_str, token_str)

            print("\nSaved to JSON and CSV!")
            print("CSV File:", SAVE_CSV)
            print("Key:\n", key_str)
            print("Encrypted Value:\n", token_str)

        elif choice == "2":
            b64 = input("Paste base64 binary data:\n> ")
            try:
                data = base64.b64decode(b64)
            except Exception:
                print("Invalid base64 input.")
                continue

            key, token = encrypt_data(data)
            name = input("Name this entry (identifier):\n> ")
            key_str = key.decode()
            token_str = token.decode()

            store[name] = {"key": key_str, "ciphertext": token_str}
            save_store(store)
            append_csv(name, key_str, token_str)

            print("\nSaved to JSON and CSV!")
            print("CSV File:", SAVE_CSV)
            print("Key:\n", key_str)
            print("Encrypted Value:\n", token_str)

        elif choice == "3":
            if not store:
                print("No saved entries.")
            else:
                print(json.dumps(store, indent=4))

        elif choice == "4":
            print("Exiting.")
            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
