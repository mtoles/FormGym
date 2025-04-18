import json
import os
from pathlib import Path
import re
from enum import Enum

def snake_to_camel_case(snake_str):
    """Convert snake_case to CamelCase"""
    components = snake_str.split('_')
    return ''.join(x.title() for x in components)

def clean_class_name(name):
    """Clean string to be used as a class name"""
    # Handle empty strings
    if not name:
        return "EmptyField"
    
    # Replace special characters with underscores
    name = re.sub(r'[^a-zA-Z0-9_]', '_', name)
    
    # Make sure it starts with a letter
    if not name[0].isalpha():
        name = 'Field_' + name
    
    # Convert ALL_CAPS to proper CamelCase
    if name.isupper():
        name = name.lower()
        name = ''.join(word.capitalize() for word in name.split('_'))
    # Convert snake_case to CamelCase if it contains underscores
    elif '_' in name:
        name = snake_to_camel_case(name)
    # Keep as is if it's already in a good format
    
    return name

def is_checkbox_dict(value):
    """Check if a dictionary represents checkbox values"""
    if not isinstance(value, dict):
        return False
    
    # Check if dictionary has checkbox-like values (containing ☑, ☐, or similar)
    for v in value.values():
        if isinstance(v, str) and (v.strip() == "☑" or v.strip() == "☐" or
                                   v.strip() == "⬛" or v.strip() == "⬜" or
                                   v.strip() == "✓" or v.strip() == "✗" or
                                   v.strip() == "\u2611" or v.strip() == "\u2610"):
            return True
    return False

def process_annotations():
    """Process all annotation JSON files and extract unique fields"""
    annotations_dir = Path('./tool/dataset/processed/annotations')
    all_fields = {}
    processed_jsons = []
    checkbox_fields = {}
    
    # Get all processed JSON files
    for json_file in annotations_dir.glob('*_processed.json'):
        print(f"Processing: {json_file}")
        with open(json_file, 'r') as f:
            data = json.load(f)
            processed_jsons.append(data)
            
            # Process each field in the JSON
            for key, value in data.items():
                if key not in all_fields:
                    all_fields[key] = []
                
                # If the value is a dictionary (nested fields from a header)
                if isinstance(value, dict):
                    # Check if it's a checkbox-like dictionary
                    if is_checkbox_dict(value):
                        # Store checkbox fields separately
                        if key not in checkbox_fields:
                            checkbox_fields[key] = {}
                        
                        # Process each checkbox option
                        for option_key, checked in value.items():
                            option_field_name = f"{key}_{option_key}"
                            if option_field_name not in checkbox_fields[key]:
                                checkbox_fields[key][option_field_name] = []
                    else:
                        # Regular nested fields
                        for nested_key, nested_value in value.items():
                            nested_field_name = f"{key}_{nested_key}"
                            if nested_field_name not in all_fields:
                                all_fields[nested_field_name] = []
    
    # Fill in values for each field from all JSONs
    for field_name in all_fields:
        for json_data in processed_jsons:
            # Check if it's a nested field
            if '_' in field_name:
                parent_key, nested_key = field_name.rsplit('_', 1)
                if parent_key in json_data and isinstance(json_data[parent_key], dict) and nested_key in json_data[parent_key]:
                    all_fields[field_name].append(json_data[parent_key][nested_key])
                else:
                    all_fields[field_name].append("")
            # Regular field
            elif field_name in json_data:
                if isinstance(json_data[field_name], list):
                    # Join list values with spaces
                    all_fields[field_name].append(' '.join(json_data[field_name]) if json_data[field_name] else "")
                else:
                    all_fields[field_name].append(json_data[field_name])
            else:
                all_fields[field_name].append("")
    
    # Process checkbox fields
    for parent_key, options in checkbox_fields.items():
        for option_field_name in options:
            checkbox_fields[parent_key][option_field_name] = []  # Reset to ensure proper ordering
            for json_data in processed_jsons:
                if parent_key in json_data and isinstance(json_data[parent_key], dict):
                    # Extract the option key from the field name
                    _, option_key = option_field_name.rsplit('_', 1)
                    
                    # Determine if checkbox is checked
                    is_checked = False
                    if option_key in json_data[parent_key]:
                        value = json_data[parent_key][option_key]
                        is_checked = (value.strip() == "☑" or value.strip() == "⬛" or 
                                     value.strip() == "✓" or value.strip() == "\u2611")
                    
                    checkbox_fields[parent_key][option_field_name].append(is_checked)
                else:
                    checkbox_fields[parent_key][option_field_name].append(False)
    
    # Remove any empty field names that might have been accidentally created
    if "" in all_fields:
        del all_fields[""]
    
    return all_fields, checkbox_fields, processed_jsons, len(processed_jsons)

def generate_form_fields(all_fields, checkbox_fields):
    """Generate form_fields.py with classes for each field"""
    output = "from fields import BaseStringField, BaseNumericField, BaseCheckboxField\n"
    output += "import user_features\n\n"
    
    # Track generated class names to prevent duplicates
    generated_classes = set()
    
    # Regular fields
    for field_name in sorted(all_fields.keys()):
        class_name = clean_class_name(field_name)
        
        # Skip if we've already generated this class
        if class_name in generated_classes:
            print(f"Warning: Skipping duplicate class {class_name} for field {field_name}")
            continue
        
        generated_classes.add(class_name)
        output += f"class {class_name}(BaseStringField):\n"
        output += "    @classmethod\n"
        output += "    def get_profile_info(cls, user_profile):\n"
        output += f"        return user_profile.features.{class_name}\n\n"
    
    # Checkbox fields
    for parent_key, options in checkbox_fields.items():
        for option_field_name in sorted(options.keys()):
            class_name = clean_class_name(option_field_name)
            
            # Skip if we've already generated this class
            if class_name in generated_classes:
                print(f"Warning: Skipping duplicate class {class_name} for field {option_field_name}")
                continue
                
            generated_classes.add(class_name)
            option_name = option_field_name.split('_')[-1]  # Get the last part after the underscore
            parent_class_name = clean_class_name(parent_key)
            
            output += f"class {class_name}(BaseCheckboxField):\n"
            output += "    @classmethod\n"
            output += "    def get_profile_info(cls, user_profile):\n"
            output += "        return (\n"
            output += f"            user_profile.features.{parent_class_name}\n"
            output += f"            == user_features.{parent_class_name}Enum.{clean_class_name(option_name)}.value\n"
            output += "        )\n\n"
    
    with open('./form_fields.py', 'w') as f:
        f.write(output)
    
    print("Generated form_fields.py")

def generate_user_profile_attributes(all_fields, checkbox_fields, processed_jsons, num_jsons):
    """Generate user_profile_attributes.py with classes for each attribute"""
    output = "from user_features import BaseUserAttr\n"
    output += "from enum import Enum\n\n"
    
    # Track generated class names to prevent duplicates
    generated_classes = set()
    
    # Generate enums for checkbox fields
    for parent_key, options in checkbox_fields.items():
        parent_class_name = clean_class_name(parent_key)
        enum_class_name = f"{parent_class_name}Enum"
        
        if enum_class_name in generated_classes:
            print(f"Warning: Skipping duplicate enum {enum_class_name} for field {parent_key}")
            continue
            
        generated_classes.add(enum_class_name)
        output += f"class {enum_class_name}(Enum):\n"
        
        for option_field_name in sorted(options.keys()):
            option_name = option_field_name.split('_')[-1]  # Get the last part after the underscore
            clean_option = clean_class_name(option_name)
            option_value = option_name.replace('_', ' ')
            output += f"    {clean_option} = \"{option_value}\"\n"
        
        output += "\n"
    
    # Generate regular attribute classes
    for field_name in sorted(all_fields.keys()):
        class_name = clean_class_name(field_name)
        
        if class_name in generated_classes:
            print(f"Warning: Skipping duplicate attribute class {class_name} for field {field_name}")
            continue
            
        generated_classes.add(class_name)
        options = all_fields[field_name]
        
        # Ensure we have the right number of options
        while len(options) < num_jsons:
            options.append("")
        
        # Truncate if we have too many options
        if len(options) > num_jsons:
            options = options[:num_jsons]
            
        # Convert all options to strings
        options = [str(option) if option is not None else "" for option in options]
        
        output += f"class {class_name}(BaseUserAttr):\n"
        output += f"    options = {repr(options)}\n\n"
        output += "    @staticmethod\n"
        output += "    def nl_desc(option):\n"
        # Use a safe display name
        safe_field_name = field_name.replace('"', '\\"') if field_name else "empty field"
        output += f"        return f\"The user's {safe_field_name}: {{option}}\"\n\n"
    
    # Generate parent classes for checkbox fields
    for parent_key in checkbox_fields:
        class_name = clean_class_name(parent_key)
        
        if class_name in generated_classes:
            print(f"Warning: Skipping duplicate parent class {class_name} for field {parent_key}")
            continue
            
        generated_classes.add(class_name)
        
        # Get all unique values across all JSONs
        all_values = []
        for json_data in processed_jsons:
            if parent_key in json_data and isinstance(json_data[parent_key], dict):
                # Find which option is checked
                checked_option = None
                for option_key, value in json_data[parent_key].items():
                    if isinstance(value, str) and (value.strip() == "☑" or value.strip() == "⬛" or 
                                  value.strip() == "✓" or value.strip() == "\u2611"):
                        checked_option = option_key
                        break
                
                if checked_option:
                    all_values.append(checked_option.replace('_', ' '))
                else:
                    all_values.append("")
            else:
                all_values.append("")
        
        # Ensure we have the right number of options
        while len(all_values) < num_jsons:
            all_values.append("")
            
        # Truncate if we have too many options
        if len(all_values) > num_jsons:
            all_values = all_values[:num_jsons]
        
        # Convert all values to strings
        all_values = [str(value) if value is not None else "" for value in all_values]
        
        output += f"class {class_name}(BaseUserAttr):\n"
        output += f"    options = {repr(all_values)}\n\n"
        output += "    @staticmethod\n"
        output += "    def nl_desc(option):\n"
        safe_field_name = parent_key.replace('"', '\\"') if parent_key else "checkbox field"
        output += f"        return f\"The user's {safe_field_name}: {{option}}\"\n\n"
    
    with open('./user_profile_attributes.py', 'w') as f:
        f.write(output)
    
    print("Generated user_profile_attributes.py")

def main():
    print("Processing annotation data...")
    all_fields, checkbox_fields, processed_jsons, num_jsons = process_annotations()
    print(f"Found {len(all_fields)} unique fields across {num_jsons} JSON files")
    print(f"Found {sum(len(options) for options in checkbox_fields.values())} checkbox options")
    
    generate_form_fields(all_fields, checkbox_fields)
    generate_user_profile_attributes(all_fields, checkbox_fields, processed_jsons, num_jsons)
    
    print("Done!")

if __name__ == "__main__":
    main()
