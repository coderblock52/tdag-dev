import json
import os

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_common_paths():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(script_dir, '..'))
    # Define common paths
    paths = {
        'root': root_dir,
        'validators': os.path.join(root_dir, 'validators'),
        'reference': os.path.join(root_dir, 'reference'),
        'generators': os.path.join(root_dir, 'generators'),
        'helpers': os.path.join(root_dir, 'helpers'),
        'roll_weights': os.path.join(root_dir, 'reference', 'roll_weights')
    }
    
    return paths

def validate_response(response, valid_keys):
    """
    Validates that the response contains only keys from the valid_keys set.
    Raises ValueError if any invalid keys are found.
    """
    invalid_keys = set(response.keys()) - set(valid_keys)
    if invalid_keys:
        raise ValueError(f"Invalid keys in response: {', '.join(invalid_keys)}")
    
    return True

def validate_value(value, valid_values):
    """
    Validates that the value is in the set of valid_values.
    Raises ValueError if the value is not valid.
    """
    if value not in valid_values:
        raise ValueError(f"Invalid value: {value}. Valid values are: {', '.join(str(valid_value) for valid_value in valid_values)}")
    
    return True

def import_all_modules_from_dir(directory, target_globals):
    import importlib.util
    import sys
    from pathlib import Path

    directory = Path(directory).resolve()

    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))

    for file in directory.glob("*.py"):
        if file.name == "__init__.py":
            continue

        module_name = file.stem
        spec = importlib.util.spec_from_file_location(module_name, file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        target_globals[module_name] = module
        sys.modules[module_name] = module
        print(f"✅ Imported module: {module_name}")

        for name in dir(module):
            if not name.startswith("_"):
                obj = getattr(module, name)
                target_globals[name] = obj
                print(f"↳ Injected: {name} from {module_name}")