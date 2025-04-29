import json
import os
from pathlib import Path
from user_profile_attributes import FormUserProfile
import form_fields

def get_json_files():
    """Get the list of JSON files in the annotations directory"""
    annotations_dir = Path('./tool/dataset/processed/annotations')
    json_files = list(annotations_dir.glob('*_processed.json'))
    return json_files

def display_user_profile(form_name=None, idx=None, json_filename=None):
    """Display a user profile and its natural language description"""
    # Create a user profile instance
    print(f"Profile Index: {idx}" if idx is not None else f"Form Name: {form_name}")
    user_profile = FormUserProfile(form_name=form_name, idx=idx)
    
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
    for field_name, field_class in form_fields.FormFieldMeta.registry.items():
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
    """Main function to demonstrate functionality"""
    # Get all JSON files
    json_files = get_json_files()
    
    if not json_files:
        print("No JSON files found. Creating a sample profile with index 0...")
        display_user_profile(idx=0)
        return
    
    # Display info for the first profile
    num_profiles = min(1, len(json_files))
    for i in range(num_profiles):
        json_file = json_files[i]
        form_name = json_file.stem  # Use filename without extension as form_name
        display_user_profile(form_name=form_name, json_filename=json_file.name)
    
    print("\n===== Another way to access the same form =====")
    print("Using index instead of form name:")
    display_user_profile(idx=0)

if __name__ == "__main__":
    main() 