import os
import pandas as pd
import itertools
import time
import math
import warnings
from import_data import import_from_text_file_using_full_path
# Suppress openpyxl warnings if they appear
warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')


def print_progress_bar(iteration, total, prefix='Progress', suffix='Complete', decimals=1, length=40, fill='█',
                       printEnd="\r"):
    """Native terminal progress bar."""
    if total == 0: return
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    if iteration == total:
        print()


def get_abs_path(file_path):
    """Returns absolute file path safely."""
    return os.path.abspath(file_path)


def load_user_file_chunked():
    """Prompts user for file path and loads it via a chunked generator."""
    while True:
        file_path = input("Enter the path to your CSV or XLSX file: ").strip().strip("'\"")
        abs_in_path = get_abs_path(file_path)

        if not os.path.exists(abs_in_path):
            print("❌ File not found. Please try again.\n")
            continue

        try:
            chunk_size = int(input("Enter chunk size for processing rows (e.g., 100): ") or 100)
        except ValueError:
            chunk_size = 100

        _, ext = os.path.splitext(abs_in_path)
        try:
            if ext.lower() == '.csv':
                return pd.read_csv(abs_in_path, chunksize=chunk_size), abs_in_path, chunk_size, ext.lower()
            elif ext.lower() == '.xlsx':
                df_full = pd.read_excel(abs_in_path)
                chunk_iter = (df_full.iloc[i:i + chunk_size] for i in range(0, len(df_full), chunk_size))
                return chunk_iter, abs_in_path, chunk_size, ext.lower()
            else:
                print("❌ Unsupported format. Please provide .csv or .xlsx\n")
        except Exception as e:
            print(f"❌ Error reading file: {e}\n")


def select_columns(df_sample):
    """Allows column selection from the target payload matrix based on a sample chunk."""
    print("\n--- Columns Found in Dataset ---")
    for idx, col in enumerate(df_sample.columns):
        print(f"...[{idx}] {col}")
    print("---------------------------------")

    while True:
        user_input = input(
            "\nEnter column numbers to include (comma-separated, e.g., '0,2') or press Enter for ALL: ").strip()
        if not user_input:
            return df_sample.columns.tolist()
        try:
            indices = [int(i.strip()) for i in user_input.split(",")]
            selected_cols = [df_sample.columns[i] for i in indices if 0 <= i < len(df_sample.columns)]
            if len(selected_cols) >= 1:
                return selected_cols
            else:
                print("⚠️ Please select at least 1 valid column.")
        except ValueError:
            print("❌ Invalid input.")


def truncate_cell(val, max_length):
    val_str = str(val)
    if len(val_str) > max_length:
        return val_str[:max_length] + "..."
    return val_str


def to_custom_markdown(df, max_cell_length):
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
                                 max_cell_length, temporal_linguistic_fiscal_path):
    total_rows = len(df)
    if not required_rows:
        return ""

    current_start = min(required_rows)
    current_end = max(required_rows)
    best_prompt = ""
    temporal_linguistic_fiscal = import_from_text_file_using_full_path(temporal_linguistic_fiscal_path)

    while True:
        slice_df = df.loc[current_start: current_end] if current_start in df.index else df.iloc[0:1]
        md_text = to_custom_markdown(slice_df, max_cell_length)
        temporal_linguistic_fiscal_sentence = " ".join(temporal_linguistic_fiscal)
        temp_prompt = (
            f"Given {observation} within the context of the full dataset {table_anchor},\n"
            f"consider the following target coordinates:\n{coordinates_block}\n\n"
            f"Here is the data payload mapping (Payload Size: {len(md_text):,} chars):\n"
            f"```markdown\n{md_text}\n```\n\n"
            f"Based on this structural snapshot, how do those specific coordinate values characterization "
            f"and/or delineate the broader trends across the dataset? Present the relationship between the previous target coordinates and the data payload mapping in a VBA, C++, and/or Python script that adequately presents said relationship into a script." +
            temporal_linguistic_fiscal_sentence
        )

        if len(temp_prompt) <= max_prompt_chars:
            best_prompt = temp_prompt
            if current_start == df.index.min() and current_end == df.index.max():
                break
        else:
            if not best_prompt:
                best_prompt = (
                    f"Given {observation} within context, target coordinates:\n{coordinates_block}\n\n"
                    f"Payload mapping (Truncated Subset):\n```markdown\n{md_text}\n```"
                )
            break

        expanded = False
        if current_start > df.index.min():
            current_start -= 1
            expanded = True
        if current_end < df.index.max():
            current_end += 1
            expanded = True

        if not expanded:
            break

    return best_prompt


def save_chunk(ledger_data, ledger_cols, base_output_name, action, chunk_idx, output_dir):
    """Flushes a processed chunk ledger to disk within a specified directory and returns absolute output path."""
    output_df = pd.DataFrame(ledger_data, columns=ledger_cols)
    out_abs_path = ""

    if action == 'txt':
        out_file = f"{base_output_name}_ledger.txt"
        out_abs_path = get_abs_path(os.path.join(output_dir, out_file))
        mode = "a" if chunk_idx > 0 else "w"
        with open(out_abs_path, mode, encoding="utf-8") as f:
            for idx, row in output_df.iterrows():
                f.write(f"=== CHUNK: {chunk_idx} | RECORD: {idx} ===\n")
                for col_name in ledger_cols:
                    f.write(f"{col_name}: {row[col_name]}\n")
                f.write("\n" + ("=" * 60) + "\n\n")

    elif action == 'csv':
        out_file = f"{base_output_name}_ledger.csv"
        out_abs_path = get_abs_path(os.path.join(output_dir, out_file))
        mode = 'a' if chunk_idx > 0 else 'w'
        header = True if chunk_idx == 0 else False
        output_df.to_csv(out_abs_path, mode=mode, header=header, index=False, encoding="utf-8")

    elif action == 'xlsx':
        out_file = f"{base_output_name}_ledger_part{chunk_idx}.xlsx"
        out_abs_path = get_abs_path(os.path.join(output_dir, out_file))
        try:
            output_df.to_excel(out_abs_path, index=False)
        except ImportError:
            out_file = f"{base_output_name}_ledger_part{chunk_idx}.csv"
            out_abs_path = get_abs_path(os.path.join(output_dir, out_file))
            output_df.to_csv(out_abs_path, index=False, encoding="utf-8")

    return out_abs_path


def process_iter_group(element_group, df_chunk, observation, table_anchor, max_prompt_chars, max_cell_length,
                       input_abs_path, epoch_now, ledger_data, gen_type, prompts_dir, chunk_idx, prompt_counter,
                       temporal_linguistic_fiscal_path):
    """Helper method to isolate processing logic. Now also writes individual prompts to .txt files."""
    combo_rows = [item[0] for item in element_group]
    callout_lines = []
    phrase_elements = []

    for r, col, val in element_group:
        trunc_val = truncate_cell(val, max_cell_length)
        callout_lines.append(f"[{col} (Unit) @ Row {r} (Value): {trunc_val}]")
        phrase_elements.append(str(val))

    coordinates_block = "\n".join(callout_lines)

    final_prompt_payload = generate_max_budgeted_prompt(
        df_chunk, combo_rows, observation, table_anchor, coordinates_block, max_prompt_chars, max_cell_length,
        temporal_linguistic_fiscal_path
    )

    # ---------------------------------------------------------
    # NEW: Write individual .txt file for this specific prompt
    # ---------------------------------------------------------
    prompt_filename = f"prompt_chunk{chunk_idx}_id{prompt_counter}.txt"
    individual_prompt_path = get_abs_path(os.path.join(prompts_dir, prompt_filename))

    with open(individual_prompt_path, 'w', encoding='utf-8') as f:
        f.write(final_prompt_payload)
    # ---------------------------------------------------------

    sample_phrase = " | ".join(phrase_elements)[:100]
    char_len = len(final_prompt_payload)
    word_len = len(final_prompt_payload.split())
    points = round((word_len / 10) * 1.5, 2)
    total_val = round(points * 1.25, 2)

    row_record = [
        input_abs_path,
        individual_prompt_path,  # Now points strictly to the written .txt file absolute path
        epoch_now,
        sample_phrase,
        char_len,
        word_len,
        min(combo_rows) if combo_rows else 0,
        combo_rows[0] if len(combo_rows) > 0 else 0,
        combo_rows[-1] if len(combo_rows) > 0 else 0,
        points,
        total_val,
        final_prompt_payload,  # Prompt is saved directly within this dedicated column in the ledger
        gen_type
    ]

    ledger_data.append(row_record)


def generate_user_prompts():
    print("=== Matrix Union Analytical Ledger Generator (Chunked & Mapped) ===")

    chunk_iter, input_abs_path, input_chunk_size, ext = load_user_file_chunked()

    # Prompt user for the path to the temporal_linguistic_fiscal variable source text file
    while True:
        temporal_linguistic_fiscal_path = input("Enter the full path to the text file for 'temporal_linguistic_fiscal': ").strip().strip("'\"")
        temporal_linguistic_fiscal_path = get_abs_path(temporal_linguistic_fiscal_path)
        if os.path.exists(temporal_linguistic_fiscal_path):
            break
        print("❌ File not found. Please try again.\n")

    if ext == '.csv':
        first_chunk = next(chunk_iter)
        chunk_iter = itertools.chain([first_chunk], pd.read_csv(input_abs_path, chunksize=input_chunk_size,
                                                                skiprows=range(1, len(first_chunk) + 1)))
    else:
        try:
            first_chunk = next(chunk_iter)
            chunk_iter = itertools.chain([first_chunk], chunk_iter)
        except StopIteration:
            print("Empty file.")
            return

    table_anchor = f"Table '{os.path.basename(input_abs_path)}' (Chunked Data Processing)"
    chosen_cols = select_columns(first_chunk)

    try:
        n_gram_cap = int(input("Enter the maximum n-gram length for cell combinations/permutations (e.g., 2): ") or 2)
        max_cell_length = int(input("Enter maximum characters per CELL preview (e.g., '50'): ") or 50)
        max_prompt_chars = int(input("Enter strict character limit for the FINAL PROMPT (e.g., '900000'): ") or 900000)
    except ValueError:
        n_gram_cap, max_cell_length, max_prompt_chars = 2, 50, 32767

    observation = input("\nEnter observation framework (e.g., '{framework}'): ").strip() or "{system behavior analysis}"

    while True:
        limit_input = input("Enter generation quota threshold per chunk (or press Enter for default 5000): ").strip()
        if not limit_input:
            execution_limit = 5000
            break
        try:
            execution_limit = int(limit_input)
            break
        except ValueError:
            print("❌ Invalid entry.")

    action = input("\nEnter documentation format output ('txt', 'csv', 'xlsx'): ").strip().lower()
    if action not in ['txt', 'csv', 'xlsx']:
        action = 'csv'

    epoch_now = int(time.time())
    base_file_name = os.path.splitext(os.path.basename(input_abs_path))[0]
    base_output_name = f"analytical_documentation_{base_file_name}_{epoch_now}"

    # Create an output directory inside the current project folder
    output_dir = os.path.join(os.getcwd(), f"Output_{base_file_name}_{epoch_now}")
    os.makedirs(output_dir, exist_ok=True)

    # Create a subfolder specifically for the individual prompt text files
    prompts_dir = os.path.join(output_dir, "Prompts")
    os.makedirs(prompts_dir, exist_ok=True)

    print(f"\n📁 Created output directory: {output_dir}")
    print(f"📁 Created prompts directory: {prompts_dir}")

    ledger_cols = [
        "Input Abs Filepath", "Output Abs Filepath", "Epoch of Entry", "Word, Phrase, Substr",
        "Length (in char)", "Length in Words", "Paragraph Index",
        "Intra-Statement Index", "Inter Statement Index",
        "Points based on quantity", "Total Value", "Generated Prompt",
        "Generation Type"
    ]

    io_mapping_table = []

    print(f"\n⚡ Processing chunks (Combinations & Permutations)...")

    chunk_idx = 0
    for df_chunk in chunk_iter:
        print(f"\n--- Processing Chunk {chunk_idx} ---")
        union_pool = []
        for r in df_chunk.index:
            for col in chosen_cols:
                union_pool.append((r, col, df_chunk.at[r, col]))

        total_elements = len(union_pool)
        if total_elements == 0:
            continue

        chunk_total_variations = 0
        for k in range(1, min(n_gram_cap + 1, total_elements + 1)):
            chunk_total_variations += math.comb(total_elements, k)
            if k > 1:
                chunk_total_variations += math.perm(total_elements, k)

        target_total = min(execution_limit, chunk_total_variations)

        ledger_data = []
        prompt_counter = 0

        print_progress_bar(0, target_total, prefix=f'Chunk {chunk_idx}', length=40)

        for k in range(1, n_gram_cap + 1):
            if prompt_counter >= execution_limit: break

            # 1. COMBINATIONS
            for element_combo in itertools.combinations(union_pool, k):
                if prompt_counter >= execution_limit: break
                process_iter_group(element_combo, df_chunk, observation, table_anchor, max_prompt_chars,
                                   max_cell_length, input_abs_path, epoch_now, ledger_data, "Combination",
                                   prompts_dir, chunk_idx, prompt_counter, temporal_linguistic_fiscal_path)
                prompt_counter += 1
                print_progress_bar(prompt_counter, target_total, prefix=f'Chunk {chunk_idx}', length=40)

            # 2. PERMUTATIONS
            if k > 1:
                for element_perm in itertools.permutations(union_pool, k):
                    if prompt_counter >= execution_limit: break
                    process_iter_group(element_perm, df_chunk, observation, table_anchor, max_prompt_chars,
                                       max_cell_length, input_abs_path, epoch_now, ledger_data, "Permutation",
                                       prompts_dir, chunk_idx, prompt_counter, temporal_linguistic_fiscal_path)
                    prompt_counter += 1
                    print_progress_bar(prompt_counter, target_total, prefix=f'Chunk {chunk_idx}', length=40)

        out_abs_path = save_chunk(ledger_data, ledger_cols, base_output_name, action, chunk_idx, output_dir)
        print(f"✅ Chunk {chunk_idx} flushed. Generative count: {prompt_counter}")
        print(f"📂 Master Ledger saved to: {out_abs_path}")

        io_mapping_table.append({
            "Input_Abs_Filepath": input_abs_path,
            "Input_Chunk_Index": chunk_idx,
            "Input_Chunk_Size": len(df_chunk),
            "Ledger_Output_Abs_Filepath": out_abs_path,
            "Items_Generated": prompt_counter
        })

        chunk_idx += 1

    mapping_df = pd.DataFrame(io_mapping_table)
    mapping_abs_path = get_abs_path(os.path.join(output_dir, f"IO_Mapping_Table_{epoch_now}.csv"))
    mapping_df.to_csv(mapping_abs_path, index=False)

    print("\n" + "=" * 50)
    print("🎯 PROCESS COMPLETE")
    print(f"📊 I/O Mapping documentation saved to: {mapping_abs_path}")
    print("=" * 50)


if __name__ == "__main__":
    generate_user_prompts()
