import os
import pandas as pd
import itertools
import time
import math


def print_progress_bar(iteration, total, prefix='Progress', suffix='Complete', decimals=1, length=40, fill='█',
                       printEnd="\r"):
    """Native terminal progress bar."""
    if total == 0:
        return
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    if iteration == total:
        print()


def load_user_file():
    """Prompts user for file path and loads it via pandas."""
    while True:
        file_path = input("Enter the path to your CSV or XLSX file: ").strip().strip("'\"")
        if not os.path.exists(file_path):
            print("❌ File not found. Please try again.\n")
            continue

        _, ext = os.path.splitext(file_path)
        try:
            if ext.lower() == '.csv':
                return pd.read_csv(file_path), file_path
            elif ext.lower() == '.xlsx':
                return pd.read_excel(file_path), file_path
            else:
                print("❌ Unsupported format. Please provide .csv or .xlsx\n")
        except Exception as e:
            print(f"❌ Error reading file: {e}\n")


def select_columns(df):
    """Allows column selection from the target payload matrix."""
    print("\n--- Columns Found in Dataset ---")
    for idx, col in enumerate(df.columns):
        print(f"...[{idx}] {col}")
    print("---------------------------------")

    while True:
        user_input = input(
            "\nEnter column numbers to include (comma-separated, e.g., '0,2') or press Enter for ALL: ").strip()
        if not user_input:
            return df.columns.tolist()

        try:
            indices = [int(i.strip()) for i in user_input.split(",")]
            selected_cols = [df.columns[i] for i in indices if 0 <= i < len(df.columns)]
            if len(selected_cols) >= 1:
                return selected_cols
            else:
                print("⚠️ Please select at least 1 valid column.")
        except ValueError:
            print("❌ Invalid input.")


def truncate_cell(val, max_length):
    """Applies the Cell Preview Length constraint safely handling non-string elements."""
    val_str = str(val)
    if len(val_str) > max_length:
        return val_str[:max_length] + "..."
    return val_str


def to_custom_markdown(df, max_cell_length):
    """Converts DataFrame slice to Markdown applying cell budget parameters."""
    headers = ["Index"] + [truncate_cell(c, max_cell_length) for c in df.columns]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |"
    ]
    for idx, row in df.iterrows():
        row_vals = [str(idx)] + [truncate_cell(val, max_cell_length) for val in row]
        lines.append("| " + " | ".join(row_vals) + " |")
    return "\n".join(lines)


def generate_max_budgeted_prompt(df, required_rows, observation, table_anchor, coordinates_block, max_prompt_chars,
                                 max_cell_length):
    """Expands bounding window around the targeted rows to fit maximum payload within context bounds."""
    total_rows = len(df)
    current_start = min(required_rows)
    current_end = max(required_rows)
    best_prompt = ""

    while True:
        slice_df = df.iloc[current_start: current_end + 1]
        md_text = to_custom_markdown(slice_df, max_cell_length)

        inc_type = "Entire Dataset" if (
                    current_start == 0 and current_end == total_rows - 1) else "Allowable Max-Budget Portion"

        temp_prompt = (
            f"Given {observation} within the context of the full dataset {table_anchor},\n"
            f"consider the following target coordinates:\n{coordinates_block}\n\n"
            f"Here is the data payload mapping ({inc_type} - Payload Size: {len(md_text):,} chars):\n"
            f"```markdown\n{md_text}\n```\n\n"
            f"Based on this structural snapshot, how do those specific coordinate values characterization "
            f"and/or delineate the broader trends across the dataset?"
        )

        if len(temp_prompt) <= max_prompt_chars:
            best_prompt = temp_prompt
            if current_start == 0 and current_end == total_rows - 1:
                break
        else:
            if not best_prompt:
                best_prompt = (
                    f"Given {observation} within context, target coordinates:\n{coordinates_block}\n\n"
                    f"Payload mapping (Truncated Subset):\n```markdown\n{md_text}\n```"
                )
            break

        expanded = False
        if current_start > 0:
            current_start -= 1
            expanded = True
        if current_end < total_rows - 1:
            current_end += 1
            expanded = True

        if not expanded:
            break

    return best_prompt


def generate_user_prompts():
    """Generates combinatorial prompts based on the absolute union of columns and rows."""
    print("=== Matrix Union Analytical Ledger Generator ===")
    df, file_path = load_user_file()
    abs_path = os.path.abspath(file_path)
    total_rows, total_cols = df.shape
    table_anchor = f"Table '{os.path.basename(file_path)}' (Dimensions: {total_rows} rows x {total_cols} columns)"

    chosen_cols = select_columns(df)

    # 1. Compile the absolute Union pool of intersecting cells
    union_pool = []
    for r in range(total_rows):
        for col in chosen_cols:
            union_pool.append((r, col, df.at[r, col]))

    total_elements = len(union_pool)
    print(f"\n✅ Created unified coordinate pool containing {total_elements} intersecting elements.")

    # Get user configuration parameters
    try:
        n_gram_cap = int(
            input(f"Enter the maximum n-gram length for cell combinations (1-{min(99, total_elements)}): ") or total_elements)
    except ValueError:
        n_gram_cap = 2

    try:
        max_cell_length = int(input("Enter maximum characters per CELL preview (e.g., '50'): ") or 50)
        max_prompt_chars = int(input("Enter strict character limit for the FINAL PROMPT (e.g., '32767'): ") or 32767)
    except ValueError:
        max_cell_length, max_prompt_chars = 50, 50000

    observation = input("\nEnter observation framework (e.g., '{framework}'): ").strip() or "{system behavior analysis}"

    # Calculate exact total of the combined union space across the requested n-gram bounds
    total_possible = sum(math.comb(total_elements, k) for k in range(1, n_gram_cap + 1))
    print(f"\n📊 PRE-CALCULATION: Total mathematical n-gram variations possible: {total_possible:,}")

    while True:
        limit_input = input(
            f"Enter generation quota threshold (or press Enter to execute all {total_possible:,}): ").strip()
        if not limit_input:
            execution_limit = total_possible
            break
        try:
            execution_limit = min(int(limit_input), total_possible)
            break
        except ValueError:
            print("❌ Invalid entry.")

    ledger_cols = [
        "abs file path of .txt", "epoch of row entry", "Word, Phrase, Substr",
        "Length (in char)", "Length in Words", "Paragraph Index",
        "Intra-Statement Index", "Inter Statement Index",
        "Global Quantity of Times Substr Appears in .txt",
        "Points based on quantity", "Total Value", "Budget Allocated"
    ]
    ledger_data = []

    print(f"\n⚡ Processing matrix unions into structural ledger database...")
    print_progress_bar(0, execution_limit, length=40)

    epoch_now = int(time.time())
    prompt_counter = 0

    # 2. Iterate dynamically over the union space lengths
    for k in range(1, n_gram_cap + 1):
        if prompt_counter >= execution_limit: break

        for element_combo in itertools.combinations(union_pool, k):
            if prompt_counter >= execution_limit: break

            # Extract rows and design coordinate text blocks from this specific variation
            combo_rows = [item[0] for item in element_combo]
            callout_lines = []
            phrase_elements = []

            for r, col, val in element_combo:
                trunc_val = truncate_cell(val, max_cell_length)
                callout_lines.append(f"[{col} (Unit) @ Row {r} (Value): {trunc_val}]")
                phrase_elements.append(str(val))

            coordinates_block = "\n".join(callout_lines)

            # Generate structurally bounded template text
            final_prompt_payload = generate_max_budgeted_prompt(
                df, combo_rows, observation, table_anchor, coordinates_block, max_prompt_chars, max_cell_length
            )

            # Calculate target documentation metrics matching requested ledger parameters
            sample_phrase = " | ".join(phrase_elements)[:100]
            char_len = len(final_prompt_payload)
            word_len = len(final_prompt_payload.split())
            global_appearances = len(df.values.ravel())
            points = round((word_len / 10) * 1.5, 2)
            total_val = round(points * 1.25, 2)

            row_record = [
                abs_path,
                epoch_now,
                sample_phrase,
                char_len,
                word_len,
                min(combo_rows),
                combo_rows[0] if len(combo_rows) > 0 else 0,
                combo_rows[-1] if len(combo_rows) > 0 else 0,
                global_appearances,
                points,
                total_val,
                final_prompt_payload
            ]

            ledger_data.append(row_record)
            prompt_counter += 1
            print_progress_bar(prompt_counter, execution_limit, length=40)

    # 3. Export Architecture Layer
    output_documentation_df = pd.DataFrame(ledger_data, columns=ledger_cols)
    print(f"\n✅ Successfully processed {len(output_documentation_df)} union records.")

    action = input("\nEnter documentation format output ('txt', 'csv', 'xlsx') or 'print': ").strip().lower()
    base_output_name = f"analytical_documentation_{os.path.splitext(os.path.basename(file_path))[0]}_{epoch_now}"

    if action == 'txt':
        out_file = f"{base_output_name}.txt"
        with open(out_file, "w", encoding="utf-8") as f:
            for idx, row in output_documentation_df.iterrows():
                f.write(f"=== RECORD ENTRY INDEX: {idx} ===\n")
                for col_name in ledger_cols:
                    f.write(f"{col_name}: {row[col_name]}\n")
                f.write("\n" + ("=" * 60) + "\n\n")
        print(f"📁 Document matrix saved to: {out_file}")

    elif action == 'csv':
        out_file = f"{base_output_name}.csv"
        output_documentation_df.to_csv(out_file, index=False, encoding="utf-8")
        print(f"📁 Ledger saved to: {out_file}")

    elif action == 'xlsx':
        out_file = f"{base_output_name}.xlsx"
        try:
            output_documentation_df.to_excel(out_file, index=False)
            print(f"📁 Spreadsheet blueprint saved to: {out_file}")
        except ImportError:
            output_documentation_df.to_csv(f"{base_output_name}.csv", index=False, encoding="utf-8")
            print("⚠️ openpyxl engine missing. Saved layout as CSV instead.")
    else:
        print("\n--- Displaying Initial Records Preview ---")
        if len(output_documentation_df) > 0:
            for col_name in ledger_cols[:-1]:
                print(f"👉 {col_name}: {output_documentation_df.iloc[0][col_name]}")
            print(f"👉 Budget Allocated:\n{output_documentation_df.iloc[0]['Budget Allocated'][:250]}...\n")


if __name__ == "__main__":
    generate_user_prompts()
