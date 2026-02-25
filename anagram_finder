import os
import shutil
import time


# ==========================================
# 1. THE LOGGER HEADER (V13.1 - Full Integration)
# ==========================================
def generate_header(summary_interval, show_console_summary):
    return f"""
# ==========================================
# ADVANCED DEBUGGER (V13.1)
# ==========================================
import datetime
import sys
import os
import builtins 
import csv
import types
import inspect
import time

_AD_DEBUG_ACTIVE = True
_ORIGINAL_PRINT = builtins.print 
_SUMMARY_INTERVAL = {summary_interval}
_SHOW_CONSOLE = {show_console_summary}
_LAST_SUMMARY_TIME = 0

if not hasattr(builtins, '_PROJECT_BASELINE_VARS'):
    builtins._PROJECT_BASELINE_VARS = set(globals().keys()) | set(dir(builtins))

def _write_to_logs(msg, log_types=["SUMMARY", "DEBUG", "SCRIPT"]):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{{log_types[0]}}] [{{timestamp}}] {{msg}}"

    # Combined Log
    try:
        with open("_COMBINED_LOG.txt", "a", encoding="utf-8") as f:
            f.write(formatted + "\\n")
    except: pass

    # Specific Logs
    for lt in log_types:
        fname = f"_{{lt}}_ONLY.txt"
        try:
            with open(fname, "a", encoding="utf-8") as f:
                f.write(formatted + "\\n")
        except: pass

def _record_state(file_path, line_no, local_vars):
    global _LAST_SUMMARY_TIME
    if not _AD_DEBUG_ACTIVE: return

    current_time = time.time()
    should_output_summary = (current_time - _LAST_SUMMARY_TIME) >= _SUMMARY_INTERVAL

    try:
        current_frame = inspect.currentframe().f_back
        func_name = current_frame.f_code.co_name
        if func_name == '<module>': return

        baseline = getattr(builtins, '_PROJECT_BASELINE_VARS', set())
        captured_data = {{}}

        for var_name, var_val in local_vars.items():
            if var_name.startswith('_') or var_name in baseline: continue
            if isinstance(var_val, (type, types.FunctionType, types.ModuleType, types.MethodType)): continue

            val_str = str(var_val).replace('\\n', ' ').replace('\\r', ' ').replace('\\t', ' ')
            sanitized_val = val_str.replace("'", "").replace("[", "").replace("]", "").strip() or "None"
            captured_data[var_name] = sanitized_val

        if not captured_data: return

        # 1. Handle CSV Output (Dynamic Columns)
        csv_file = "_VARIABLE_MATRIX.csv"
        file_exists = os.path.isfile(csv_file) and os.path.getsize(csv_file) > 0

        fieldnames = ["Timestamp", "File", "Line", "Function"]
        existing_rows = []

        if file_exists:
            try:
                with open(csv_file, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    if reader and reader.fieldnames:
                        fieldnames = list(reader.fieldnames)
                    existing_rows = list(reader)
            except: pass

        # Update headers if new variables found
        new_vars = [v for v in captured_data.keys() if v not in fieldnames]
        if new_vars:
            fieldnames.extend(new_vars)

        # Write/Update CSV
        row = {{"Timestamp": datetime.datetime.now().strftime("%H:%M:%S"), 
               "File": os.path.basename(file_path), 
               "Line": line_no, 
               "Function": func_name, 
               **captured_data}}

        with open(csv_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
            writer.writeheader()
            writer.writerows(existing_rows + [row])

        # 2. Handle Text Summary (Based on Interval)
        if should_output_summary:
            summary_msg = f"Line {{line_no}} ({{func_name}}): " + ", ".join([f"{{k}}={{v}}" for k,v in captured_data.items()])
            _write_to_logs(summary_msg, log_types=["SUMMARY"])
            if _SHOW_CONSOLE:
                _ORIGINAL_PRINT(f"[SUMMARY] {{summary_msg}}")
            _LAST_SUMMARY_TIME = current_time

    except Exception as e:
        _ORIGINAL_PRINT(f"[DEBUG_INTERNAL_ERR] {{e}}")

def _ad_script_output(msg, is_error=True):
    l_type = "DEBUG" if is_error else "SCRIPT"
    _write_to_logs(msg, log_types=[l_type])
    _ORIGINAL_PRINT(f"[{{l_type}}] {{msg}}")

def print(*args, **kwargs):
    _ad_script_output(" ".join(map(str, args)), is_error=False)
# ==========================================
"""


# ==========================================
# 2. THE PRE-PROCESSOR
# ==========================================
def clean_source(source):
    result, i, n = [], 0, len(source)
    quote_type, in_comment, last_valuable_char = None, False, ""
    while i < n:
        char = source[i]
        if in_comment:
            if char == '\n': in_comment = False; result.append('\n')
            i += 1;
            continue
        if quote_type:
            if quote_type in ('"""', "'''"):
                if source[i:i + 3] == quote_type:
                    result.append(quote_type);
                    quote_type = None;
                    i += 3;
                    continue
                else:
                    result.append(char); i += 1
            else:
                if char == quote_type and (i == 0 or source[i - 1] != '\\'):
                    result.append(char);
                    quote_type = None
                else:
                    result.append(char)
                i += 1
            continue
        if source[i:i + 3] in ('"""', "'''"):
            quote_type = source[i:i + 3];
            result.append(quote_type);
            i += 3
        elif char in ('"', "'"):
            quote_type = char;
            result.append(char);
            i += 1
        elif char == '#':
            in_comment = True;
            i += 1
        else:
            if not char.isspace(): last_valuable_char = char
            result.append(char);
            i += 1
    return "".join(result)


# ==========================================
# 3. THE INJECTION ENGINE
# ==========================================
def inject_into_file(file_path, interval, show_console, max_depth=3):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_content = f.read()

        clean_content = clean_source(raw_content)
        lines = clean_content.splitlines()
        new_content = [generate_header(interval, show_console)]
        bracket_level, in_triple_quote = 0, False

        for i, line in enumerate(lines):
            stripped = line.strip()
            if not stripped:
                new_content.append(line);
                continue

            triple_count = line.count('"""') + line.count("'''")
            starts_or_ends_triple = triple_count % 2 != 0
            indent_str = line[:len(line) - len(line.lstrip())]

            prev_level = bracket_level
            bracket_level += (line.count('(') + line.count('[') + line.count('{'))
            bracket_level -= (line.count(')') + line.count(']') + line.count('}'))

            structural = ('def ', 'class ', 'if ', 'elif ', 'else:', 'for ', 'while ', 'with ', 'try:', 'except',
                          'finally:', '@', 'import ', 'from ')
            is_structural = any(stripped.startswith(k) for k in structural) or stripped.endswith(':')

            # Determine depth by indent (4 spaces per level)
            current_depth = len(indent_str) // 4

            if not in_triple_quote and prev_level == 0 and bracket_level == 0 and not is_structural and current_depth <= max_depth:
                if stripped in (")", "]", "}", "),", "],", "},") or starts_or_ends_triple:
                    new_content.append(line)
                else:
                    new_content.append(f"{indent_str}try:")
                    new_content.append(f"{indent_str}    {stripped}")
                    new_content.append(f"{indent_str}    _record_state(__file__, {i + 1}, locals())")
                    new_content.append(
                        f"{indent_str}except Exception as e: _ad_script_output(f'Line {i + 1} Err: {{e}}')")
            else:
                new_content.append(line)

            if starts_or_ends_triple: in_triple_quote = not in_triple_quote

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(new_content))
    except Exception as e:
        print(f"Injection Engine Error on {file_path}: {e}")


# ==========================================
# 4. RUNNER
# ==========================================
def run():
    p = input("Project Path: ").strip().strip('"')
    if not os.path.isdir(p):
        print("Invalid path.")
        return

    try:
        interval = int(input("Summary Interval (seconds, e.g. 30): ") or 0)
        show_cons = input("Show Summary in Console? (y/n): ").lower() == 'y'
        depth = int(input("Max Depth (default 3): ") or 3)
    except ValueError:
        print("Invalid input for interval or depth. Using defaults.")
        interval, show_cons, depth = 0, True, 3

    t_dir = p.rstrip('\\/') + f"_DEBUG_{int(time.time())}"
    os.makedirs(t_dir, exist_ok=True)

    print(f"\n[START] Building project...")
    for root, _, files in os.walk(p):
        # Skip common non-source directories
        if any(x in root for x in ['venv', '.git', '__pycache__', '.idea', '.vscode']):
            continue

        for file in files:
            if file.endswith(".py"):
                src = os.path.join(root, file)
                dst = os.path.join(t_dir, os.path.relpath(src, p))
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(src, dst)
                inject_into_file(dst, interval, show_cons, depth)
                print(f"  Instrumented: {file}")

    print(f"\n[FINISH] Project ready at: {t_dir}")
    print("Files to look for in your project folder after running:")
    print("  - _VARIABLE_MATRIX.csv (Pivot table of all variables)")
    print("  - _COMBINED_LOG.txt (All logs)")
    print("  - _SUMMARY_ONLY.txt, _DEBUG_ONLY.txt, _SCRIPT_ONLY.txt")


if __name__ == "__main__":
    run()
