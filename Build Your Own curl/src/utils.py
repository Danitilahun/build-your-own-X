import json
import argparse

def json_or_string(value):
    
    try:
        return json.loads(value)
    
    except json.JSONDecodeError:
        return value
    
def key_value_pair(value):
    try:
        key, val = value.split(':', 1)
        return (key.strip(), val.strip())
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{value}' is not a valid Key:Value header.")
