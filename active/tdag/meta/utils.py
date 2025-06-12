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
        'helpers': os.path.join(root_dir, 'helpers')
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
        raise ValueError(f"Invalid value: {value}. Valid values are: {', '.join(valid_values)}")
    
    return True

