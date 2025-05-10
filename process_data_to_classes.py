import json
import os
from pathlib import Path
import re
from enum import Enum
from user_profile_attributes import FormUserProfile, FormUserAttributeMeta, FormUserAttr
import form_fields as form_field_types  # Rename the import to avoid conflict

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
    """Normalize field name by removing whitespace, special characters and converting to consistent case"""
    if not name:
        return ""
    # Convert to lowercase and remove whitespace
    name = re.sub(r'\s+', '', name.lower())
    # Remove special characters except underscores
    name = re.sub(r'[^a-z0-9_]', '', name)
    return name

def process_annotations():
    """Process all annotation JSON files and extract unique fields"""
    annotations_dir = Path('./tool/dataset/processed/funsd/annotations')
    all_fields = {}
    processed_jsons = []
    json_file_paths = []  # Keep track of the original file paths in order
    checkbox_fields = {}
    
    # Get all processed JSON files
    for json_file in annotations_dir.glob('*_processed.json'):
        json_file_paths.append(json_file)
    
    # Sort the JSON files to ensure consistent ordering
    json_file_paths.sort()
    
    # Process each JSON file
    for json_file in json_file_paths:
        print(f"Processing: {json_file}")
        with open(json_file, 'r') as f:
            data = json.load(f)
            form_name = json_file.stem  # Use the filename (without extension) as the form name
            
            # Initialize form data in all_fields
            if form_name not in all_fields:
                all_fields[form_name] = {}
            
            # Track normalized field names for this form to handle merging
            normalized_fields = {}
            
            # Process each field in the JSON directly for this form
            for key, value in data.items():
                # Skip empty keys
                if not key:
                    continue
                
                # Normalize the key
                normalized_key = normalize_field_name(key)
                if not normalized_key:
                    continue
                
                # Check if we've already seen this normalized key in this form
                if normalized_key in normalized_fields:
                    # Get the existing value
                    existing_value = all_fields[form_name].get(normalized_key)
                    
                    # If both values are dictionaries, merge them
                    if isinstance(value, dict) and isinstance(existing_value, dict):
                        all_fields[form_name][normalized_key].update(value)
                        print(f"Merged dictionary values for fields in form {form_name}: '{key}' and '{normalized_fields[normalized_key]}' (normalized to '{normalized_key}')")
                    # If both are lists, extend the list
                    elif isinstance(value, list) and isinstance(existing_value, list):
                        all_fields[form_name][normalized_key].extend(value)
                        print(f"Merged list values for fields in form {form_name}: '{key}' and '{normalized_fields[normalized_key]}' (normalized to '{normalized_key}')")
                    # If one is a dictionary and the other isn't, keep them separate with suffixes
                    elif isinstance(value, dict) or isinstance(existing_value, dict):
                        # Create unique keys for both values
                        key1 = f"{normalized_key}_1"
                        key2 = f"{normalized_key}_2"
                        # Store both values with their unique keys
                        all_fields[form_name][key1] = existing_value if existing_value is not None else ""
                        all_fields[form_name][key2] = value
                        # Remove the original key if it exists
                        if normalized_key in all_fields[form_name]:
                            del all_fields[form_name][normalized_key]
                        print(f"Split different-type values for fields in form {form_name}: '{key}' and '{normalized_fields[normalized_key]}' into '{key1}' and '{key2}'")
                    else:
                        # For other types, if they're different, keep both with suffixes
                        if existing_value != value:
                            key1 = f"{normalized_key}_1"
                            key2 = f"{normalized_key}_2"
                            all_fields[form_name][key1] = existing_value if existing_value is not None else ""
                            all_fields[form_name][key2] = value
                            # Remove the original key if it exists
                            if normalized_key in all_fields[form_name]:
                                del all_fields[form_name][normalized_key]
                            print(f"Split different values for fields in form {form_name}: '{key}' and '{normalized_fields[normalized_key]}' into '{key1}' and '{key2}'")
                    continue
                
                normalized_fields[normalized_key] = key
                
                # Handle dictionaries (nested fields or checkboxes)
                if isinstance(value, dict):
                    # Check if it's a checkbox-like dictionary
                    if is_checkbox_dict(value):
                        if form_name not in checkbox_fields:
                            checkbox_fields[form_name] = {}
                        
                        # Add parent checkbox field
                        checkbox_fields[form_name][normalized_key] = {}
                        
                        # Process each checkbox option
                        for option_key, checked in value.items():
                            normalized_option_key = normalize_field_name(option_key)
                            option_field_name = f"{normalized_key}_{normalized_option_key}"
                            is_checked = isinstance(checked, str) and (
                                checked.strip() == "☑" or 
                                checked.strip() == "⬛" or 
                                checked.strip() == "✓" or 
                                checked.strip() == "\u2611"
                            )
                            checkbox_fields[form_name][normalized_key][option_field_name] = is_checked
                    else:
                        # Regular nested fields
                        all_fields[form_name][normalized_key] = value
                else:
                    # Handle array values by joining them with spaces
                    if isinstance(value, list):
                        all_fields[form_name][normalized_key] = ' '.join(value) if value else ""
                    else:
                        all_fields[form_name][normalized_key] = value
            
            processed_jsons.append((form_name, data))
    
    # Get the list of all form names for reference
    all_form_names = list(all_fields.keys())
    
    return all_fields, checkbox_fields, processed_jsons, all_form_names

def create_dynamic_classes(all_fields, checkbox_fields, all_form_names):
    """Dynamically create classes for form fields and user profile attributes"""
    # Track generated class names to prevent duplicates
    generated_classes = set()
    
    # Create classes for regular fields for each form
    for form_name, field_values in all_fields.items():
        for field_name, field_value in field_values.items():
            # Create a unique class name for this field and form
            safe_field_name = clean_class_name(field_name)
            class_name = f"{safe_field_name}_{form_name}"
            
            # Skip if we've already generated this class
            if class_name in generated_classes:
                print(f"Warning: Duplicate class name generated: {class_name}")
                continue
            
            generated_classes.add(class_name)
            
            # Create a closure to capture the current class_name
            def make_get_profile_info(class_name):
                def get_profile_info(cls, user_profile):
                    return getattr(user_profile.features, class_name)
                return classmethod(get_profile_info)
            
            # Create the form field class
            form_field_class = type(class_name, (form_field_types.FormBaseStringField,), {
                'get_profile_info': make_get_profile_info(class_name)
            })
            
            # Add to registry
            form_field_types.FormFieldMeta.registry[class_name] = form_field_class
            
            # Create the user profile attribute class
            # Only include value for this specific form
            values = {form_name: field_value}
            
            # Create a closure to capture the field_name
            def make_nl_desc(field_name):
                def nl_desc(option):
                    safe_field_name = field_name.replace('"', '\\"') if field_name else "empty field"
                    return f"The user's {safe_field_name}: {option}"
                return staticmethod(nl_desc)
            
            # Create user attribute class with same name as form field class
            user_attr_class = type(class_name, (FormUserAttr,), {
                'values': values,
                'nl_desc': make_nl_desc(field_name)
            })
            
            # Add to registry
            FormUserAttributeMeta.registry[class_name] = user_attr_class
    
    # Create checkbox field classes
    for form_name, form_checkboxes in checkbox_fields.items():
        for parent_key, options in form_checkboxes.items():
            # Create a unique class name for the parent checkbox field
            safe_parent_key = clean_class_name(parent_key)
            parent_class_name = f"{safe_parent_key}_{form_name}"
            
            # Skip if we've already generated this class
            if parent_class_name in generated_classes:
                print(f"Warning: Skipping duplicate class {parent_class_name} for field {parent_key} in form {form_name}")
                continue
                
            generated_classes.add(parent_class_name)
            
            # Create enum class for checkbox options
            enum_members = {}
            for option_field_name in sorted(options.keys()):
                option_name = option_field_name.replace(f"{parent_key}_", "")
                clean_option = clean_class_name(option_name)
                enum_members[clean_option] = option_name
            
            # Create enum class properly
            enum_class = Enum(f"{parent_class_name}Enum", enum_members)
            
            # Determine the checked option for this form
            checked_option = None
            for option_field_name, is_checked in options.items():
                if is_checked:
                    option_name = option_field_name.replace(f"{parent_key}_", "")
                    checked_option = option_name
                    break
            
            # Create parent user attribute class
            def make_parent_nl_desc(parent_key):
                def nl_desc(option):
                    safe_field_name = parent_key.replace('"', '\\"') if parent_key else "checkbox field"
                    return f"The user's {safe_field_name}: {option}"
                return staticmethod(nl_desc)
            
            # Create parent user attribute class
            values = {form_name: checked_option if checked_option else ""}
            
            parent_attr_class = type(parent_class_name, (FormUserAttr,), {
                'values': values,
                'nl_desc': make_parent_nl_desc(parent_key)
            })
            
            # Add to registry
            FormUserAttributeMeta.registry[parent_class_name] = parent_attr_class
            
            # Create checkbox option classes
            for option_field_name, is_checked in options.items():
                # Create a unique class name for each checkbox option
                safe_option_field_name = clean_class_name(option_field_name)
                option_class_name = f"{safe_option_field_name}_{form_name}"
                
                # Skip if we've already generated this class
                if option_class_name in generated_classes:
                    print(f"Warning: Skipping duplicate class {option_class_name} for field {option_field_name} in form {form_name}")
                    continue
                    
                generated_classes.add(option_class_name)
                option_name = option_field_name.replace(f"{parent_key}_", "")
                clean_option = clean_class_name(option_name)
                
                # Create a closure to capture the current values
                def make_checkbox_get_profile_info(parent_class_name, enum_class, clean_option):
                    def get_profile_info(cls, user_profile):
                        try:
                            parent_value = getattr(user_profile.features, parent_class_name)
                            return parent_value == getattr(enum_class, clean_option).value
                        except (AttributeError, KeyError):
                            return False
                    return classmethod(get_profile_info)
                
                # Create the form field class
                form_field_class = type(option_class_name, (form_field_types.FormBaseCheckboxField,), {
                    'get_profile_info': make_checkbox_get_profile_info(parent_class_name, enum_class, clean_option)
                })
                
                # Add to registry
                form_field_types.FormFieldMeta.registry[option_class_name] = form_field_class
                
                # Create user attribute class for the option
                option_values = {form_name: is_checked}
                
                def make_option_nl_desc(option_name):
                    def option_nl_desc(option):
                        safe_option_name = option_name.replace('"', '\\"') if option_name else "checkbox option"
                        return f"The user's {safe_option_name}: {option}"
                    return staticmethod(option_nl_desc)
                
                # Create user attribute class for the option
                option_attr_class = type(option_class_name, (FormUserAttr,), {
                    'values': option_values,
                    'nl_desc': make_option_nl_desc(option_name)
                })
                
                # Add to registry
                FormUserAttributeMeta.registry[option_class_name] = option_attr_class

def write_meta_class_outputs(all_form_names):
    """Write output files using meta classes instead of reading JSONs directly"""
    output_dir = Path('./tool/dataset/processed/funsd/outputs')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for form_name in all_form_names:
        output_file = output_dir / f"{form_name}.txt"
        with open(output_file, 'w') as f:
            f.write(f"Form: {form_name}\n")
            f.write("=" * 50 + "\n\n")
            
            # Create a user profile for this form
            user_profile = FormUserProfile(form_name=form_name)
            
            # Get all form fields for this form
            form_field_entries = []
            for field_name, field_class in form_field_types.FormFieldMeta.registry.items():
                if field_name.endswith(f"_{form_name}"):
                    try:
                        field_value = field_class.get_profile_info(user_profile)
                        if field_value is not None:
                            form_field_entries.append((field_name, field_value))
                    except (AttributeError, TypeError, ValueError):
                        continue
            
            # Sort fields by name for consistent output
            form_field_entries.sort(key=lambda x: x[0])
            
            # Write field values
            for field_name, field_value in form_field_entries:
                if isinstance(field_value, dict):
                    f.write(f"{field_name}:\n")
                    for subkey, subvalue in sorted(field_value.items()):
                        f.write(f"  {subkey}: {subvalue}\n")
                else:
                    f.write(f"{field_name}: {field_value}\n")
                f.write("\n")

def display_user_profile(form_name, json_filename=None):
    """Display a user profile and its natural language description"""
    # Create a user profile instance
    print(f"Form Name: {form_name}")
    user_profile = FormUserProfile(form_name=form_name)
    
    print(f"\n===== User Profile: {user_profile.form_name} =====")
    if json_filename:
        print(f"Source JSON: {json_filename}")
    
    # Get and display natural language profile description
    print("\nNatural Language Profile:")
    nl_profile = user_profile.get_nl_profile()
    for desc in nl_profile:
        if desc.strip() and not desc.endswith(": "):
            print(f"- {desc}")
    
    # Display common user attributes
    print("\nUser Profile Key Attributes:")
    
    # Show user profile attributes that we've found in the natural language description
    common_attributes = []
    for attr in dir(user_profile.features):
        if not attr.startswith('__') and hasattr(user_profile.features, attr):
            value = getattr(user_profile.features, attr)
            if value and str(value).strip():  # Only show non-empty values
                common_attributes.append((attr, value))
    
    # Print the top 10 attributes (or fewer if there aren't that many)
    for i, (attr, value) in enumerate(common_attributes[:10]):
        print(f"- {attr}: {value}")
    
    # Example of accessing form fields mapped to this profile
    print("\nForm Field Values for this Profile:")
    
    # Find form fields that would work with this profile
    found_fields = 0
    for field_name, field_class in form_field_types.FormFieldMeta.registry.items():
        if field_name.endswith(f"_{form_name}"):  # Only show fields for this form
            try:
                field_value = field_class.get_profile_info(user_profile)
                if field_value and str(field_value).strip():  # Only show non-empty values
                    print(f"- {field_name}: {field_value}")
                    found_fields += 1
            except (AttributeError, TypeError, ValueError):
                # Skip fields that don't work with this profile
                continue
    
    return user_profile

def main():
    print("Processing annotation data...")
    all_fields, checkbox_fields, processed_jsons, all_form_names = process_annotations()
    print(f"Found {len(all_fields)} unique forms")
    
    # Create dynamic classes
    create_dynamic_classes(all_fields, checkbox_fields, all_form_names)
    
    # Write outputs using meta classes
    write_meta_class_outputs(all_form_names)
    
    # Display info for each profile
    for form_name, json_data in processed_jsons:
        display_user_profile(form_name=form_name, json_filename=f"{form_name}.json")
        print("\n" + "="*50 + "\n")
    
    print("Done!")

if __name__ == "__main__":
    main()
