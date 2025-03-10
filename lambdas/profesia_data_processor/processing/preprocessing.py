import logging

from config import name_replacements


def preprocess(data_dict: dict) -> dict:
    data_dict = convert_dict_to_lowercase(data_dict)
    data_dict = convert_nested_key_to_int(data_dict)
    data_dict = rename_dict_keys(data_dict, name_replacements)

    return data_dict


def convert_nested_key_to_int(data_dict: dict, key_to_convert: str) -> dict:
    """Converts all key_to_convert values in a 1 nested dictonary to an int"""
    for key, value in data_dict.items():
        data_dict[key] = convert_key_to_int(value, key_to_convert)

    return data_dict


def rename_dict_keys(data_dict: dict, key_mapping: dict) -> dict:
    """Renames the keys in dictionary based on the key_mapping dictionary."""
    renamed_dict = {}
    
    for key, value in data_dict.items():
        # Rename the key if it's in the mapping, else keep the original key
        new_key = key_mapping.get(key, key).lower()
        
        # If the value is a dictionary, rename its keys
        if isinstance(value, dict):
            value = {key_mapping.get(k, k): v for k, v in value.items()}
        
        renamed_dict[new_key] = value
    
    return renamed_dict


def convert_dict_to_lowercase(d):
    """Converts an entire dictionary to lowercase"""
    if isinstance(d, dict):
        return {k.lower(): convert_dict_to_lowercase(v) for k, v in d.items()}
    elif isinstance(d, list):
        return [convert_dict_to_lowercase(i) for i in d]
    elif isinstance(d, str):
        return d.lower()
    else:
        return d



def convert_key_to_int(data_dict: dict, key_to_convert: str) -> dict:
    """Converts all key_to_convert values in a dictionary to an intager"""
    for key, value in data_dict.items():
        if key_to_convert in value:
            try:
                value[key_to_convert] = int(value[key_to_convert].strip().replace(" ", ""))
            except (ValueError, TypeError) as e:
                logging.error(f"Converting count {value.get(key_to_convert)} to int failed for key: {key}. Error: {e}")
                raise

    return data_dict

