"""
Helper functions for RPAL Language
General-purpose utility functions used across the project.
"""

def convert_string_to_bool(data):
    """
    Convert a string to a boolean.
    
    Args:
        data: The string to convert
        
    Returns:
        bool: The converted boolean
    """
    if data == "true":
        return True
    elif data == "false":
        return False
    return None