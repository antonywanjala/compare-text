
# ==========================================
# AUTO-DEBUGGER INJECTION START
# ==========================================
import inspect
import os
import types

def _ad_logger(original_line, local_vars, active=True):
    if not active:
        return

    frame = inspect.currentframe().f_back
    code_obj = frame.f_code
    func_name = code_obj.co_name
    abs_path = os.path.abspath(code_obj.co_filename)
    filename = os.path.basename(abs_path)
    debug_exec_line = frame.f_lineno
    func_start_line = code_obj.co_firstlineno

    if func_name == '<module>':
        rel_line = debug_exec_line
        display_func = "Main Script"
        offset_str = f"Line {rel_line}" 
    else:
        rel_line = debug_exec_line - func_start_line
        display_func = func_name
        offset_str = f"+{rel_line} (inside {display_func})"

    include_globals = True
    vars_to_show = local_vars.copy()

    if include_globals:
        for k, v in frame.f_globals.items():
            if k not in vars_to_show:
                vars_to_show[k] = v

    summary_parts = []

    # Standard primitive types that should display their VALUE
    primitives = (int, float, str, bool, type(None), list, dict, set, tuple)

    for k, v in vars_to_show.items():
        if k.startswith('_') or k in ('local_vars', 'In', 'Out'):
            continue

        # 1. Filter out Modules and Functions entirely
        if isinstance(v, (types.ModuleType, types.FunctionType, types.BuiltinFunctionType)):
            continue

        try:
            # 2. Check if it is a primitive (Value) or an Object (Description)
            if isinstance(v, primitives):
                summary_parts.append(f"{k} = {repr(v)}")
            else:
                # It is a complex object/class instance
                cls_name = type(v).__name__
                # Get the module (file) where the class is defined
                origin = getattr(v, '__module__', 'unknown_source')
                summary_parts.append(f"{k} is an instantiation of {cls_name} from {origin}")

        except:
            continue

    var_string = ", ".join(summary_parts)

    print(f"\n[DEBUG] {filename} | {display_func}")
    print(f"   Positions: Orig {original_line} | Debug {debug_exec_line} | Offset {offset_str}")
    if var_string:
        print(f"   Variables: {var_string}")
# ==========================================
# AUTO-DEBUGGER INJECTION END
# ==========================================
_ad_logger(1, locals())
import os
_ad_logger(2, locals())
import shutil
_ad_logger(3, locals())
import time
_ad_logger(4, locals())
import ast
_ad_logger(5, locals())
import datetime


# ==========================================
# 0. SESSION LOGGER (Captures Console Output)
# ==========================================
_ad_logger(11, locals())
class SessionLogger:
    _ad_logger(12, locals())
    def __init__(self):
        _ad_logger(13, locals())
        self.logs = []

    _ad_logger(15, locals())
    def log(self, message=""):
        _ad_logger(16, locals())
        print(message)
        _ad_logger(17, locals())
        self.logs.append(message)

    _ad_logger(19, locals())
    def save_report(self, target_dir):
        _ad_logger(20, locals())
        report_path = os.path.join(target_dir, "_DEBUG_SUMMARY.txt")
        header = f"""
==================================================
      DEBUG INJECTION REPORT
      Generated: {datetime.datetime.now()}
==================================================
_ad_logger(26, locals())
"""
        _ad_logger(27, locals())
        with open(report_path, 'w', encoding='utf-8') as f:
            _ad_logger(28, locals())
            f.write(header + "\n")
            _ad_logger(29, locals())
            f.write("\n".join(self.logs))
        _ad_logger(30, locals())
        print(f"\n[REPORT] Summary saved to: {report_path}")


_ad_logger(33, locals())
logger = SessionLogger()


# ==========================================
# 1. THE LOGGER HEADER (Modified for Object Identification)
# ==========================================
_ad_logger(39, locals())
def generate_header(include_globals=False):
    _ad_logger(40, locals())
    globals_flag = "True" if include_globals else "False"

    return f"""
# ==========================================
# AUTO-DEBUGGER INJECTION START
# ==========================================
import inspect
import os
import types

def _ad_logger(original_line, local_vars, active=True):
    if not active:
        return

    frame = inspect.currentframe().f_back
    code_obj = frame.f_code
    func_name = code_obj.co_name
    abs_path = os.path.abspath(code_obj.co_filename)
    filename = os.path.basename(abs_path)
    debug_exec_line = frame.f_lineno
    func_start_line = code_obj.co_firstlineno

    if func_name == '<module>':
        rel_line = debug_exec_line
        display_func = "Main Script"
        offset_str = f"Line {{rel_line}}" 
    else:
        rel_line = debug_exec_line - func_start_line
        display_func = func_name
        offset_str = f"+{{rel_line}} (inside {{display_func}})"

    include_globals = {globals_flag}
    vars_to_show = local_vars.copy()

    if include_globals:
        for k, v in frame.f_globals.items():
            if k not in vars_to_show:
                vars_to_show[k] = v

    summary_parts = []

    # Standard primitive types that should display their VALUE
    primitives = (int, float, str, bool, type(None), list, dict, set, tuple)

    for k, v in vars_to_show.items():
        if k.startswith('_') or k in ('local_vars', 'In', 'Out'):
            continue

        # 1. Filter out Modules and Functions entirely
        if isinstance(v, (types.ModuleType, types.FunctionType, types.BuiltinFunctionType)):
            continue

        try:
            # 2. Check if it is a primitive (Value) or an Object (Description)
            if isinstance(v, primitives):
                summary_parts.append(f"{{k}} = {{repr(v)}}")
            else:
                # It is a complex object/class instance
                cls_name = type(v).__name__
                # Get the module (file) where the class is defined
                origin = getattr(v, '__module__', 'unknown_source')
                summary_parts.append(f"{{k}} is an instantiation of {{cls_name}} from {{origin}}")

        except:
            continue

    var_string = ", ".join(summary_parts)

    print(f"\\n[DEBUG] {{filename}} | {{display_func}}")
    print(f"   Positions: Orig {{original_line}} | Debug {{debug_exec_line}} | Offset {{offset_str}}")
    if var_string:
        print(f"   Variables: {{var_string}}")
# ==========================================
# AUTO-DEBUGGER INJECTION END
# ==========================================
_ad_logger(115, locals())
"""


# ==========================================
# 2. INJECTION LOGIC (Unchanged)
# ==========================================
_ad_logger(121, locals())
def inject_into_file(file_path, mode_choice, include_globals):
    _ad_logger(122, locals())
    try:
        _ad_logger(123, locals())
        with open(file_path, 'r', encoding='utf-8') as f:
            _ad_logger(124, locals())
            lines = f.readlines()

        _ad_logger(126, locals())
        new_content = [generate_header(include_globals)]
        _ad_logger(127, locals())
        bracket_level = 0
        _ad_logger(128, locals())
        in_multiline_string = False

        _ad_logger(130, locals())
        for i, line in enumerate(lines):
            _ad_logger(131, locals())
            stripped = line.strip()
            _ad_logger(132, locals())
            indent = line[:len(line) - len(line.lstrip())]
            _ad_logger(133, locals())
            original_line_num = i + 1

            bracket_level += (stripped.count('(') + stripped.count('[') + stripped.count('{'))
            _ad_logger(136, locals())
            bracket_level -= (stripped.count(')') + stripped.count(']') + stripped.count('}'))
            if '"""' in stripped or "'''" in stripped:
                _ad_logger(138, locals())
                if (stripped.count('"""') % 2 != 0) or (stripped.count("'''") % 2 != 0):
                    _ad_logger(139, locals())
                    in_multiline_string = not in_multiline_string

            is_continuation = any(stripped.startswith(w) for w in ('else', 'elif', 'except', 'finally', ')', ']', '}'))
            is_safe_zone = (bracket_level == 0 and not in_multiline_string)

            should_inject = False
            if is_safe_zone and stripped and not stripped.startswith(('#', '@')) and not is_continuation:
                if mode_choice == '1':
                    should_inject = True
                elif mode_choice == '2' and "# DEBUG" in line:
                    should_inject = True

            if should_inject:
                new_content.append(f"{indent}_ad_logger({original_line_num}, locals())\n")
            new_content.append(line)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_content)
        return True
    except Exception as e:
        logger.log(f"[ERROR] Failed to process {file_path}: {e}")
        return False


# ==========================================
# 3. DEPENDENCY & RANGE PARSERS
# ==========================================
def find_local_dependencies(target_files, all_project_files_map):
    dependencies = set()
    for file_path in target_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read())

            for node in ast.walk(tree):
                module_name = None
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        module_name = alias.name
                elif isinstance(node, ast.ImportFrom):
                    module_name = node.module

                if module_name:
                    potential_path = module_name.replace('.', os.sep)
                    for rel_path, full_path in all_project_files_map.items():
                        if rel_path.startswith(potential_path):
                            dependencies.add((rel_path, full_path))
        except:
            continue
    return list(dependencies)


def parse_selection(selection_str, max_index):
    selection_str = selection_str.strip()
    if selection_str.lower() == 'all':
        return list(range(max_index))

    selected_indices = set()
    parts = selection_str.split(',')

    for part in parts:
        part = part.strip()
        if '-' in part:
            try:
                start, end = map(int, part.split('-'))
                for i in range(start - 1, end):
                    if 0 <= i < max_index:
                        selected_indices.add(i)
            except:
                pass
        else:
            try:
                idx = int(part) - 1
                if 0 <= idx < max_index:
                    selected_indices.add(idx)
            except:
                pass
    return sorted(list(selected_indices))


# ==========================================
# 4. MAIN PROCESS
# ==========================================
def process_project(source_dir, mode_choice, include_globals):
    dir_name = os.path.basename(os.path.normpath(source_dir))
    target_dir = os.path.join(os.path.dirname(os.path.normpath(source_dir)), f"{dir_name}_{str(time.time())}_debug_build")

    if os.path.exists(target_dir):
        logger.log(f"Cleaning old build at: {target_dir}")
        shutil.rmtree(target_dir)

    logger.log(f"Cloning project to: {target_dir} ...")
    shutil.copytree(source_dir, target_dir)

    ignored_dirs = {'venv', 'env', '.git', '__pycache__', 'site-packages', 'node_modules', 'dist', 'build'}
    py_files = []
    file_map = {}

    logger.log("\n--- Scanning Project Structure ---")
    for root, dirs, files in os.walk(target_dir):
        dirs[:] = [d for d in dirs if d not in ignored_dirs]
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, target_dir)
                py_files.append((rel_path, full_path))
                file_map[rel_path] = full_path

    if not py_files:
        logger.log("[ERROR] No .py files found!")
        return

    logger.log(f"Found {len(py_files)} User-Created Python files:")
    for idx, (rel, full) in enumerate(py_files):
        logger.log(f"[{idx + 1}] {rel}")

    logger.log("\nWhich MAIN files do you want to debug? (e.g., '1-3' or 'all')")
    selection = input("Enter selection: ").strip()
    logger.log(f"> User Selection: {selection}")

    indices_to_inject = parse_selection(selection, len(py_files))
    selected_files_paths = [py_files[i][1] for i in indices_to_inject]

    logger.log("\n--- Analyzing Dependencies ---")
    local_deps = find_local_dependencies(selected_files_paths, file_map)
    new_deps = [d for d in local_deps if d[1] not in selected_files_paths]

    final_injection_list = set(selected_files_paths)

    if new_deps:
        logger.log(f"[Detected Imports] These files are imported by your selection:")
        for rel, full in new_deps:
            logger.log(f" - {rel}")

        confirm = input("Include these dependencies? (y/n): ").strip().lower()
        logger.log(f"> Include Dependencies: {confirm}")

        if confirm == 'y':
            for _, full in new_deps:
                final_injection_list.add(full)
    else:
        logger.log("No additional local dependencies found.")

    logger.log("\n--- Injection Status ---")
    injected_count = 0
    copied_count = 0

    for rel, full_path in py_files:
        if full_path in final_injection_list:
            if inject_into_file(full_path, mode_choice, include_globals):
                logger.log(f"[INJECTED] {rel}")
                injected_count += 1
        else:
            logger.log(f"[COPIED]   {rel}")
            copied_count += 1

    logger.log(f"\nDONE. {injected_count} files injected, {copied_count} files copied silently.")
    logger.log(f"Debug Build Location: {target_dir}")

    logger.save_report(target_dir)


def main():
    logger.log("--- Object-Aware Debugger with Reporting ---")
    raw_path = input("Enter path to your Project Folder: ").strip()
    input_path = raw_path.strip('"').strip("'")
    logger.log(f"> Target Path: {input_path}")

    if not os.path.exists(input_path) or not os.path.isdir(input_path):
        logger.log("Error: Valid directory path required.")
        return

    logger.log("\nDebug Mode: 1.Full Trace | 2.Selective (# DEBUG)")
    mode_choice = input("Select mode (1 or 2): ").strip()
    logger.log(f"> Mode: {mode_choice}")

    logger.log("\nScope: 1.Local only | 2.Global + Local")
    scope_choice = input("Select scope (1 or 2): ").strip()
    include_globals = (scope_choice == '2')
    logger.log(f"> Scope: {scope_choice}")

    process_project(input_path, mode_choice, include_globals)


if __name__ == "__main__":
    main()
