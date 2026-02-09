
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
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
_ad_logger(5, locals())
from sample_from_script_main import sample_function
_ad_logger(6, locals())
from sample_script_class_from_main import SampleClass

_ad_logger(8, locals())
def calculate_complex_metric(data):
    # TODO: Write this algorithm later
    _ad_logger(10, locals())
    raise NotImplementedError("This function is not yet implemented.")

_ad_logger(12, locals())
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    _ad_logger(14, locals())
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    _ad_logger(15, locals())
    var1 = 0
    _ad_logger(16, locals())
    var2 = 1
    _ad_logger(17, locals())
    var3 = 3
    _ad_logger(18, locals())
    try:
        _ad_logger(19, locals())
        var5 = 4
        _ad_logger(20, locals())
        calculate_complex_metric(var5)
    except Exception as e:
        _ad_logger(22, locals())
        print(e)
    _ad_logger(23, locals())
    var6 = 7
    _ad_logger(24, locals())
    var7 = 8
    _ad_logger(25, locals())
    var8 = 9


# Press the green button in the gutter to run the script.
_ad_logger(29, locals())
if __name__ == '__main__':
    _ad_logger(30, locals())
    print_hi('PyCharm')
    _ad_logger(31, locals())
    variable1 = sample_function()
    _ad_logger(32, locals())
    obj = SampleClass()
    _ad_logger(33, locals())
    variable2 = obj.calculate()
    _ad_logger(34, locals())
    print(variable2)  # Output: 6
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
