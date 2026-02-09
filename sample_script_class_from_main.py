
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
class SampleClass:
    _ad_logger(2, locals())
    def __init__(self):
        # The variables are defined when the class is initialized
        _ad_logger(4, locals())
        self.var1 = 1
        _ad_logger(5, locals())
        self.var2 = 2
        _ad_logger(6, locals())
        self.var3 = 3

    _ad_logger(8, locals())
    def calculate(self):
        # The method accesses the variables stored in 'self'
        _ad_logger(10, locals())
        return self.var1 + self.var2 + self.var3

# Usage
"""
obj = SampleClass()
print(obj.calculate())  # Output: 6
_ad_logger(16, locals())
"""