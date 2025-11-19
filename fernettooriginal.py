from cryptography.fernet import Fernet, InvalidToken
import base64

def main():
    print("\nFernet Decryption Utility")
    print("--------------------------")

    while True:
        print("\nChoose an option:")
        print("1. Decrypt text")
        print("2. Exit")
        choice = input("> ").strip()

        if choice == "1":
            key_input = input("\nEnter your Fernet key:\n> ").strip()
            token_input = input("\nEnter the Fernet-encrypted value (ciphertext):\n> ").strip()

            try:
                # Convert to bytes
                key = key_input.encode()
                token = token_input.encode()

                f = Fernet(key)
                decrypted = f.decrypt(token)

                # Attempt text decode; fallback to bytes
                try:
                    out = decrypted.decode()
                except UnicodeDecodeError:
                    out = f"[Binary Output] base64: {base64.b64encode(decrypted).decode()}"

                print("\nDecrypted Output:")
                print(out)

            except (InvalidToken, ValueError, base64.binascii.Error):
                print("\nERROR: Invalid key or ciphertext. Decryption failed.")

        elif choice == "2":
            print("Exiting.")
            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
