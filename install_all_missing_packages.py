import os
import sys
import subprocess
import importlib.util
from typing import Set, Optional, List, Union

# Mappings now support lists for ambiguous imports
COMMON_MAPPINGS = {
}


def is_standard_library(module_name: str) -> bool:
    if module_name in sys.builtin_module_names:
        return True
    if hasattr(sys, 'stdlib_module_names'):
        return module_name in sys.stdlib_module_names

    # Use standard library sysconfig or fallback to setuptools.sysconfig
    try:
        import sysconfig
        std_lib_path = sysconfig.get_path("stdlib")
    except (ImportError, AttributeError):
        from setuptools import sysconfig
        std_lib_path = sysconfig.get_python_lib(standard_lib=True)

    return os.path.exists(os.path.join(std_lib_path, f"{module_name}.py")) or \
        os.path.exists(os.path.join(std_lib_path, module_name))


def is_installed(module_name: str, python_exe: str) -> bool:
    if python_exe == sys.executable:
        try:
            return importlib.util.find_spec(module_name) is not None
        except (ImportError, ValueError, AttributeError):
            return False

    try:
        subprocess.check_call(
            [python_exe, "-c", f"import {module_name}"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return True
    except subprocess.CalledProcessError:
        return False


def get_imports_from_file(filepath: str) -> Set[str]:
    imports = set()
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.split('#')[0].strip()
                if not line:
                    continue

                if line.startswith('from '):
                    import_idx = line.find(' import ')
                    if import_idx != -1:
                        module_path = line[5:import_idx].strip()
                        base_module = module_path.split('.')[0].strip()
                        if base_module and not base_module.startswith('.'):
                            imports.add(base_module)
                    continue

                if line.startswith('import '):
                    modules_str = line[7:].strip()
                    for mod in modules_str.split(','):
                        mod = mod.strip()
                        if ' as ' in mod:
                            mod = mod.split(' as ')[0].strip()
                        base_module = mod.split('.')[0].strip()
                        if base_module:
                            imports.add(base_module)

    except Exception as e:
        print(f"⚠️ Warning: Could not read file '{filepath}': {e}")

    return imports


def resolve_local_module(base_dir: str, module_name: str) -> Optional[str]:
    py_file = os.path.join(base_dir, f"{module_name}.py")
    if os.path.isfile(py_file):
        return py_file

    init_file = os.path.join(base_dir, module_name, "__init__.py")
    if os.path.isfile(init_file):
        return init_file

    return None


def find_all_dependencies(abs_script_path: str) -> Set[str]:
    base_dir = os.path.dirname(abs_script_path)
    files_to_process = [abs_script_path]
    processed_files = set()
    third_party_deps = set()

    while files_to_process:
        current_file = files_to_process.pop(0)
        if current_file in processed_files:
            continue

        processed_files.add(current_file)
        file_imports = get_imports_from_file(current_file)

        for imp in file_imports:
            if is_standard_library(imp):
                continue

            local_path = resolve_local_module(base_dir, imp)
            if local_path:
                if local_path not in processed_files:
                    files_to_process.append(local_path)
            else:
                third_party_deps.add(imp)

    return third_party_deps


def prompt_user_package_choices(missing_imports: List[str]) -> List[str]:
    """Resolves ambiguities and lets the user override PyPI package names."""
    planned_installs = {}

    # Phase 1: Resolve Ambiguities First
    for imp in missing_imports:
        mapped = COMMON_MAPPINGS.get(imp, [imp])

        if len(mapped) > 1:
            print(f"\n⚠️  Ambiguous import detected: 'import {imp}'")
            print("   Multiple PyPI packages use this import name. Which one do you want?")
            for i, opt in enumerate(mapped, 1):
                print(f"   [{i}] {opt}")
            print(f"   [{len(mapped) + 1}] Enter a custom name")
            print(f"   [{len(mapped) + 2}] Skip this package")

            while True:
                choice = input("Select an option: ").strip()
                if choice.isdigit():
                    idx = int(choice)
                    if 1 <= idx <= len(mapped):
                        planned_installs[imp] = mapped[idx - 1]
                        break
                    elif idx == len(mapped) + 1:
                        planned_installs[imp] = input(f"Enter custom package name for '{imp}': ").strip()
                        break
                    elif idx == len(mapped) + 2:
                        break
                print("Invalid selection. Try again.")
        else:
            planned_installs[imp] = mapped[0]

    if not planned_installs:
        return []

    # Phase 2: Final Review and Edit
    print("\n--------------------------------------------------")
    print("📋 Planned Installations:")
    idx = 1
    for imp, pkg in planned_installs.items():
        if imp == pkg:
            print(f"  [{idx}] import {imp:<15} -> pip install {pkg}")
        else:
            print(f"  [{idx}] import {imp:<15} -> pip install {pkg} (Mapped)")
        idx += 1
    print("--------------------------------------------------")
    print("Options:")
    print("  • Press ENTER to install all planned packages as listed")
    print("  • Type 'edit' to manually correct a PyPI package name")
    print("  • Type '0' or 'none' to cancel completely")

    choice = input("\nYour selection: ").strip().lower()

    if choice in ('0', 'none', 'n'):
        return []

    if choice == 'edit':
        print("\n✏️  Manual Override Mode")
        print("Type the correct PyPI name. Press ENTER to keep the default. Type 'skip' to ignore it.")

        final_packages = []
        for imp, pkg in planned_installs.items():
            override = input(f"  Package for 'import {imp}' [default: {pkg}]: ").strip()
            if override.lower() == 'skip':
                continue
            final_packages.append(override if override else pkg)
        return final_packages

    return list(planned_installs.values())


def install_missing_packages(raw_path: str, python_exe: str = sys.executable):
    abs_path = os.path.abspath(os.path.expanduser(raw_path))

    if not os.path.exists(abs_path):
        print(f"❌ Error: File does not exist:\n   {abs_path}")
        sys.exit(1)

    if not os.path.exists(python_exe):
        print(f"❌ Error: Target Python interpreter does not exist:\n   {python_exe}")
        sys.exit(1)

    print(f"🎯 Target File: {abs_path}")
    print(f"🐍 Target Interpreter: {python_exe}")
    print("🔍 Scanning file and local imports for missing dependencies...")

    deps = find_all_dependencies(abs_path)

    if not deps:
        print("✅ No third-party dependencies found.")
        return

    missing_imports = []
    for dep in deps:
        if not is_installed(dep, python_exe):
            missing_imports.append(dep)

    if not missing_imports:
        print("✅ All required packages are already installed in the target environment.")
        return

    selected_for_install = prompt_user_package_choices(missing_imports)

    if not selected_for_install:
        print("⏭️ Installation skipped by user.")
        return

    print(f"\n📦 Proceeding to install {len(selected_for_install)} package(s): {', '.join(selected_for_install)}\n")

    for package in selected_for_install:
        print(f"⏳ Installing {package}...")
        try:
            subprocess.check_call([python_exe, "-m", "pip", "install", package])
            print(f"✅ Successfully installed {package}")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package}. Verify the package name on PyPI.")


def preset1(target_path: Optional[str] = None, custom_env: Optional[str] = None):
    # Default to the current running script if no target path is provided
    if not target_path:
        target_path = __file__

    # Default to the current Python executable if no custom environment is provided
    target_env = custom_env if custom_env else sys.executable

    install_missing_packages(target_path, target_env)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        target_path = input("Enter the full absolute file path to your Python script: ").strip()
        custom_env = input("Enter path to target Python interpreter (press Enter to use current): ").strip()
        target_env = custom_env if custom_env else sys.executable
    elif len(sys.argv) == 2:
        target_path = sys.argv[1]
        target_env = sys.executable
    elif len(sys.argv) >= 3:
        target_path = sys.argv[1]
        target_env = sys.argv[2]

    install_missing_packages(target_path, target_env)
