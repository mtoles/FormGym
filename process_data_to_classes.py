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
    
    # Check for Python keywords and add prefix if needed
    python_keywords = ["False", "None", "True", "and", "as", "assert", "async", "await", 
                      "break", "class", "continue", "def", "del", "elif", "else", "except", 
                      "finally", "for", "from", "global", "if", "import", "in", "is", 
                      "lambda", "nonlocal", "not", "or", "pass", "raise", "return", 
                      "try", "while", "with", "yield"]
    
    if name in python_keywords:
        name = "Field" + name
    
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

def normalize_field_name(name):
    """Normalize field name by removing whitespace and converting to lowercase"""
    if not name:
        return ""
    # Remove whitespace and convert to lowercase for consistent comparison
    return re.sub(r'\s+', '', name).lower()

def process_annotations():
    """Process all annotation JSON files and extract unique fields"""
    annotations_dir = Path('./tool/dataset/processed/annotations')
    all_fields = {}
    normalized_field_map = {}  # Maps normalized field names to original field names
    processed_jsons = []
    json_file_paths = []  # Keep track of the original file paths in order
    checkbox_fields = {}
    
    # Get all processed JSON files
    for json_file in annotations_dir.glob('*_processed.json'):
        json_file_paths.append(json_file)
    
    # Sort the JSON files to ensure consistent ordering
    json_file_paths.sort()
    
    # First pass: collect all field names and their normalized versions
    for json_file in json_file_paths:
        with open(json_file, 'r') as f:
            data = json.load(f)
            for key in data.keys():
                normalized_key = normalize_field_name(key)
                if normalized_key:
                    # Keep track of all original field names that map to the same normalized name
                    if normalized_key not in normalized_field_map:
                        normalized_field_map[normalized_key] = key
                    
                    # For nested fields, also normalize the parent key
                    if isinstance(data[key], dict):
                        for nested_key in data[key].keys():
                            normalized_nested_key = f"{normalized_key}_{normalize_field_name(nested_key)}"
                            if normalized_nested_key not in normalized_field_map:
                                normalized_field_map[normalized_nested_key] = f"{key}_{nested_key}"
    
    # Process each JSON file
    for json_file in json_file_paths:
        print(f"Processing: {json_file}")
        with open(json_file, 'r') as f:
            data = json.load(f)
            form_name = json_file.stem  # Use the filename (without extension) as the form name
            processed_jsons.append((form_name, data))
            
            # Process each field in the JSON
            for key, value in data.items():
                normalized_key = normalize_field_name(key)
                if not normalized_key:
                    continue  # Skip empty keys
                
                # Get the canonical field name for this normalized key
                canonical_key = normalized_field_map[normalized_key]
                
                # Initialize the field if needed
                if canonical_key not in all_fields:
                    all_fields[canonical_key] = {}
                
                # If the value is a dictionary (nested fields from a header)
                if isinstance(value, dict):
                    # Check if it's a checkbox-like dictionary
                    if is_checkbox_dict(value):
                        # Store checkbox fields separately
                        if canonical_key not in checkbox_fields:
                            checkbox_fields[canonical_key] = {}
                        
                        # Process each checkbox option
                        for option_key, checked in value.items():
                            normalized_option_key = normalize_field_name(option_key)
                            option_field_name = f"{canonical_key}_{option_key}"
                            normalized_option_field_name = f"{normalized_key}_{normalized_option_key}"
                            
                            # Use the canonical name for this normalized option field
                            if normalized_option_field_name in normalized_field_map:
                                option_field_name = normalized_field_map[normalized_option_field_name]
                            
                            if option_field_name not in checkbox_fields[canonical_key]:
                                checkbox_fields[canonical_key][option_field_name] = {}
                    else:
                        # Regular nested fields
                        for nested_key, nested_value in value.items():
                            normalized_nested_key = normalize_field_name(nested_key)
                            nested_field_name = f"{canonical_key}_{nested_key}"
                            normalized_nested_field_name = f"{normalized_key}_{normalized_nested_key}"
                            
                            # Use the canonical name for this normalized nested field
                            if normalized_nested_field_name in normalized_field_map:
                                nested_field_name = normalized_field_map[normalized_nested_field_name]
                            
                            if nested_field_name not in all_fields:
                                all_fields[nested_field_name] = {}
    
    # Fill in values for each field from all JSONs
    for form_name, json_data in processed_jsons:
        # Process all fields in the JSON
        for key, value in json_data.items():
            normalized_key = normalize_field_name(key)
            if not normalized_key:
                continue
                
            # Get the canonical field name
            canonical_key = normalized_field_map[normalized_key]
            
            # Process regular fields
            if canonical_key in all_fields:
                if isinstance(value, list):
                    # Join list values with spaces
                    all_fields[canonical_key][form_name] = ' '.join(value) if value else ""
                elif not isinstance(value, dict):  # Skip dictionaries as they're processed separately
                    all_fields[canonical_key][form_name] = value
            
            # Process nested fields
            if isinstance(value, dict):
                for nested_key, nested_value in value.items():
                    normalized_nested_key = normalize_field_name(nested_key)
                    nested_field_name = f"{canonical_key}_{nested_key}"
                    normalized_nested_field_name = f"{normalized_key}_{normalized_nested_key}"
                    
                    # Check if we have a canonical name for this nested field
                    if normalized_nested_field_name in normalized_field_map:
                        nested_field_name = normalized_field_map[normalized_nested_field_name]
                    
                    # Add to all_fields if it's a regular nested field
                    if nested_field_name in all_fields:
                        all_fields[nested_field_name][form_name] = nested_value
                        
                # Process checkbox fields
                if canonical_key in checkbox_fields:
                    for option_field_name in checkbox_fields[canonical_key]:
                        option_key = option_field_name.split('_', 1)[1]  # Get the part after the first underscore
                        
                        # Check if the option is checked
                        is_checked = False
                        if option_key in value:
                            check_value = value[option_key]
                            if isinstance(check_value, str) and (check_value.strip() == "☑" or check_value.strip() == "⬛" or 
                                          check_value.strip() == "✓" or check_value.strip() == "\u2611"):
                                is_checked = True
                        
                        checkbox_fields[canonical_key][option_field_name][form_name] = is_checked
    
    # Remove any empty field names that might have been accidentally created
    if "" in all_fields:
        del all_fields[""]
    
    # Get the list of all form names for reference
    all_form_names = [form_name for form_name, _ in processed_jsons]
    
    return all_fields, checkbox_fields, processed_jsons, all_form_names

def generate_form_fields(all_fields, checkbox_fields):
    """Generate form_fields.py with classes for each field"""
    output = "import user_profile_attributes\n"
    output += "from typing import List\n"
    output += "from abc import ABC, abstractmethod\n\n"
    
    output += "def numerize(s):\n"
    output += "    ls = list(s)\n"
    output += "    valid = [\"0\", \"1\", \"2\", \"3\", \"4\", \"5\", \"6\", \"7\", \"8\", \"9\", \".\"]\n"
    output += "    return str([x for x in ls if x in valid])\n\n\n"
    
    output += "def remove_punctuation(s):\n"
    output += "    # replace punctuation with space\n"
    output += "    s = \"\".join(\n"
    output += "        \" \" if c in \"!\\\"#$%&'()*+,-./:;<=>?@[\\\\]^_`{|}~ \\t\\n\\r\\x0b\\x0c\" else c\n"
    output += "        for c in s\n"
    output += "    )\n"
    output += "    # replace all whitespace with spaces\n"
    output += "    s = \" \".join(s.split())\n"
    output += "    return s\n\n\n"
    
    output += "def concat_agent_generations(agent_generations):\n"
    output += "    return \" \".join(\n"
    output += "        [\n"
    output += "            x[\"value\"]\n"
    output += "            for x in sorted(\n"
    output += "                agent_generations, key=lambda item: (item[\"cy\"], item[\"cx\"])\n"
    output += "            )\n"
    output += "        ]\n"
    output += "    )\n\n\n"
    
    output += "def get_inputs_inside_field(field, agent_generations):\n"
    output += "    return [\n"
    output += "        ag\n"
    output += "        for ag in agent_generations\n"
    output += "        if (\n"
    output += "            ag[\"cx\"] >= field.x\n"
    output += "            and ag[\"cx\"] <= field.x + field.w\n"
    output += "            and ag[\"cy\"] >= field.y\n"
    output += "            and ag[\"cy\"] <= field.y + field.h\n"
    output += "        )\n"
    output += "    ]\n\n\n"
    
    output += "class FormFieldMeta(type):\n"
    output += "    \"\"\"\n"
    output += "    Metaclass for possible form fields\n"
    output += "    \"\"\"\n\n"
    output += "    registry = {}\n\n"
    output += "    def __new__(cls, name, bases, attrs):\n"
    output += "        new_p_attr = super().__new__(cls, name, bases, attrs)\n"
    output += "        base_classes = [\"FormBaseField\", \"FormBaseNumericField\", \"FormBaseStringField\", \"FormBaseCheckboxField\", \"FormAnnotatedField\", \"FormSignOrInitial\", \"FormSignature\", \"FormInitials\"]\n"
    output += "        if name not in base_classes:\n"
    output += "            # check for duplicates\n"
    output += "            assert name not in cls.registry, f\"Form field {name} already exists\"\n"
    output += "            cls.registry[name] = new_p_attr\n"
    output += "        return new_p_attr\n\n\n"
    
    output += "class FormBaseField(metaclass=FormFieldMeta):\n"
    output += "    def __init__(self, x, y, w, h):\n"
    output += "        self.x = x\n"
    output += "        self.y = y\n"
    output += "        self.w = w\n"
    output += "        self.h = h\n\n"
    output += "    @abstractmethod\n"
    output += "    def is_correct(self, agent_generation, user_profile):\n"
    output += "        raise NotImplementedError\n\n"
    output += "    @classmethod\n"
    output += "    @abstractmethod\n"
    output += "    def get_profile_info(cls, user_profile):\n"
    output += "        raise NotImplementedError\n\n\n"
    
    output += "class FormBaseNumericField(FormBaseField):\n"
    output += "    # def is_correct(self, agent_generation, user_profile):\n"
    output += "    def is_correct(self, agent_generation, user_profile):\n"
    output += "        agent_generations_inside = get_inputs_inside_field(self, agent_generation)\n"
    output += "        concatted_input = concat_agent_generations(agent_generations_inside)\n"
    output += "        profile_info = self.get_profile_info(user_profile)\n"
    output += "        return numerize(profile_info) == numerize(concatted_input)\n\n\n"
    
    output += "class FormBaseStringField(FormBaseField):\n"
    output += "    # def is_correct(self, agent_generation, user_profile):\n"
    output += "    def is_correct(self, agent_generation, user_profile):\n"
    output += "        agent_generations_inside = get_inputs_inside_field(self, agent_generation)\n"
    output += "        concatted_input = concat_agent_generations(agent_generations_inside)\n"
    output += "        profile_info = self.get_profile_info(user_profile)\n"
    output += "        return remove_punctuation(profile_info) == remove_punctuation(concatted_input)\n\n\n"
    
    output += "class FormBaseCheckboxField(FormBaseField):\n"
    output += "    # def is_correct(self, agent_generation, user_profile):\n"
    output += "    def is_correct(self, agent_generation, user_profile):\n"
    output += "        agent_generations_inside = get_inputs_inside_field(self, agent_generation)\n"
    output += "        concatted_input = concat_agent_generations(agent_generations_inside)\n"
    output += "        profile_info = self.get_profile_info(user_profile)\n"
    output += "        assert isinstance(profile_info, bool)\n"
    output += "        if profile_info:\n"
    output += "            return concatted_input == \"x\"\n"
    output += "        else:\n"
    output += "            return concatted_input == \"\"\n\n\n"
    
    output += "class FormAnnotatedField(FormBaseField):\n"
    output += "    pass\n\n\n"
    
    output += "class FormSignOrInitial(FormBaseField):\n"
    output += "    def is_correct(self, agent_generation, user_profile):\n"
    output += "        agent_generations_inside = get_inputs_inside_field(self, agent_generation)\n"
    output += "        if len(agent_generations_inside) != 1:\n"
    output += "            return False\n"
    output += "        agent_gen = agent_generations_inside[0]\n"
    output += "        if agent_gen[\"action\"] != \"Sign\":\n"
    output += "            return False\n"
    output += "        signature_val = agent_gen[\"value\"]\n"
    output += "        profile_info = self.get_profile_info(user_profile)\n"
    output += "        return profile_info == signature_val\n\n\n"
    
    output += "class FormSignature(FormSignOrInitial):\n"
    output += "    @classmethod\n"
    output += "    def get_profile_info(cls, user_profile):\n"
    output += "        return user_profile.features.FirstName + \" \" + user_profile.features.LastName\n\n\n"
    
    output += "class FormInitials(FormSignOrInitial):\n"
    output += "    @classmethod\n"
    output += "    def get_profile_info(cls, user_profile):\n"
    output += "        return user_profile.features.FirstName[0] + user_profile.features.LastName[0]\n\n\n"
    
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
        output += f"class {class_name}(FormBaseStringField):\n"
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
            
            output += f"class {class_name}(FormBaseCheckboxField):\n"
            output += "    @classmethod\n"
            output += "    def get_profile_info(cls, user_profile):\n"
            output += "        return (\n"
            output += f"            user_profile.features.{parent_class_name}\n"
            output += f"            == user_profile_attributes.{parent_class_name}Enum.{clean_class_name(option_name)}.value\n"
            output += "        )\n\n"
    
    with open('./form_fields.py', 'w') as f:
        f.write(output)
    
    print("Generated form_fields.py")

def generate_user_profile_attributes(all_fields, checkbox_fields, processed_jsons, all_form_names):
    """Generate user_profile_attributes.py with classes for each attribute"""
    output = f"""from enum import Enum

class FormUserAttributeMeta(type):
    registry = {{}}

    def __new__(cls, name, bases, attrs):
        new_p_attr = super().__new__(cls, name, bases, attrs)
        if name not in ["FormUserAttr"]:
            assert name not in cls.registry, f"User attribute {{name}} already exists"
            cls.registry[name] = new_p_attr
        return new_p_attr


class FormUserProfile:
    def __init__(self, form_name=None, idx=None):
        class Features:
            pass

        self.features = Features()
        
        # If form_name is provided, use it directly
        if form_name is not None:
            self.form_name = form_name
        # Otherwise, use the index to find the form name
        elif idx is not None and idx < len(self.all_form_names):
            self.form_name = self.all_form_names[idx]
        else:
            # Default to first form if invalid index
            self.form_name = self.all_form_names[0] if self.all_form_names else "unknown"
        
        for name, attr_class in FormUserAttributeMeta.registry.items():
            if hasattr(attr_class, "values") and isinstance(attr_class.values, dict):
                # Get the value for this form, or empty string if not found
                value = attr_class.values.get(self.form_name, "")
                setattr(self.features, name, value)
            else:
                raise AttributeError(f"Class {{name}} must have a 'values' dictionary.")

    def get_nl_profile(self):
        nl_profile = []
        for name, attr_class in FormUserAttributeMeta.registry.items():
            nl_profile.append(attr_class.nl_desc(getattr(self.features, name)))
        return nl_profile
    
    # Store all form names for reference
    all_form_names = {all_form_names}


class FormUserAttr(metaclass=FormUserAttributeMeta):
    pass

"""
    
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
        
        # Track used enum values to prevent duplicates
        used_enum_values = set()
        used_enum_names = set()
        
        for option_field_name in sorted(options.keys()):
            option_name = option_field_name.split('_')[-1]  # Get the last part after the underscore
            clean_option = clean_class_name(option_name)
            
            # Check for duplicate enum member names
            if clean_option in used_enum_names:
                clean_option = f"{clean_option}_{len(used_enum_names)}"
            used_enum_names.add(clean_option)
            
            option_value = option_name.replace('_', ' ')
            
            # Check for duplicate enum values
            if option_value in used_enum_values:
                option_value = f"{option_value} ({len(used_enum_values)})"
            used_enum_values.add(option_value)
            
            output += f"    {clean_option} = \"{option_value}\"\n"
        
        output += "\n"
    
    # Generate regular attribute classes
    for field_name in sorted(all_fields.keys()):
        class_name = clean_class_name(field_name)
        
        if class_name in generated_classes:
            print(f"Warning: Skipping duplicate attribute class {class_name} for field {field_name}")
            continue
            
        generated_classes.add(class_name)
        values = all_fields[field_name]
        
        # Convert all values to strings
        string_values = {k: str(v) if v is not None else "" for k, v in values.items()}
        
        output += f"class {class_name}(FormUserAttr):\n"
        output += f"    values = {repr(string_values)}\n\n"
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
        
        # Get all values across all JSONs
        checked_values = {}
        for form_name, json_data in processed_jsons:
            if parent_key in json_data and isinstance(json_data[parent_key], dict):
                # Find which option is checked
                checked_option = None
                for option_key, value in json_data[parent_key].items():
                    if isinstance(value, str) and (value.strip() == "☑" or value.strip() == "⬛" or 
                                  value.strip() == "✓" or value.strip() == "\u2611"):
                        checked_option = option_key
                        break
                
                if checked_option:
                    checked_values[form_name] = checked_option.replace('_', ' ')
                else:
                    checked_values[form_name] = ""
        
        output += f"class {class_name}(FormUserAttr):\n"
        output += f"    values = {repr(checked_values)}\n\n"
        output += "    @staticmethod\n"
        output += "    def nl_desc(option):\n"
        safe_field_name = parent_key.replace('"', '\\"') if parent_key else "checkbox field"
        output += f"        return f\"The user's {safe_field_name}: {{option}}\"\n\n"
    
    with open('./user_profile_attributes.py', 'w') as f:
        f.write(output)
    
    print("Generated user_profile_attributes.py")

def main():
    print("Processing annotation data...")
    all_fields, checkbox_fields, processed_jsons, all_form_names = process_annotations()
    print(f"Found {len(all_fields)} unique fields across {len(all_form_names)} JSON files")
    print(f"Found {sum(len(options) for options in checkbox_fields.values())} checkbox options")
    
    generate_form_fields(all_fields, checkbox_fields)
    generate_user_profile_attributes(all_fields, checkbox_fields, processed_jsons, all_form_names)
    
    print("Done!")

if __name__ == "__main__":
    main()
