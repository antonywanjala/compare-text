import nltk
import csv

# Download the necessary punctuation model (runs quietly)
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab')

def process_text_to_csv(input_filepath, output_filepath):
    try:
        # 1. Read the raw text file
        with open(input_filepath, 'r', encoding='utf-8') as file:
            text = file.read()

        # 2. Tokenize the text into intelligent statements
        statements = nltk.sent_tokenize(text)

        # 3. Create and write to the new CSV file
        # Note: newline='' is important to prevent blank rows in Windows
        with open(output_filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)

            # Write our header row
            writer.writerow(['Index', 'Statement', 'Number of Words', 'Number of Characters'])

            # Process and write each statement
            for index, statement in enumerate(statements, 1):
                # Strip leading/trailing whitespace for clean data
                clean_statement = statement.strip()

                # Calculate metrics
                # Splitting by space is a standard, lightweight way to count words
                word_count = len(clean_statement.split())
                char_count = len(clean_statement)

                # Write the row
                writer.writerow([index, clean_statement, word_count, char_count])

        print(f"Success! {len(statements)} statements have been saved to '{output_filepath}'.")

    except FileNotFoundError:
        print(f"Error: Could not find the file '{input_filepath}'. Please check the path.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# ==========================================
# Usage
# ==========================================

# Replace these strings with your actual file names/paths
input_document = input("Enter absolute path to .txt: ")
output_spreadsheet = 'processed_statements_' + str(time.time()) + '.csv'

process_text_to_csv(input_document, output_spreadsheet)