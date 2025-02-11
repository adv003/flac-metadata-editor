import logging
import argparse
import sys
from mutagen.flac import FLAC, FLACNoHeaderError

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('flac_editor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def print_metadata(metadata):
    if metadata:
        print("\nFLAC Metadata:")
        print("-" * 40)
        for key, value in metadata.items():
            print(f"{key}: {value}")
        print("-" * 40)
    else:
        print("No metadata found or error reading metadata")

def read_metadata(file_path):
    try:
        flac = FLAC(file_path)
        return dict(flac.tags)
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return None
    except FLACNoHeaderError:
        logger.error(f"Invalid FLAC file: {file_path}")
        return None
    except Exception as e:
        logger.exception(f"Unexpected error reading {file_path}: {e}")
        return None

def validate_metadata_input(new_metadata):
    valid_entries = {}
    if not isinstance(new_metadata, dict):
        logger.error("new_metadata must be a dictionary")
        return valid_entries

    for key, value in new_metadata.items():
        if isinstance(value, str):
            if value.strip():
                valid_entries[key] = [value]
            else:
                logger.warning(f"Empty string for key {key}. Skipping.")
        elif isinstance(value, list):
            if all(isinstance(v, str) and v.strip() != '' for v in value):
                valid_entries[key] = value
            else:
                logger.warning(f"Invalid list for key {key}. Contains non-string or empty values. Skipping.")
        else:
            logger.warning(f"Invalid value type for key {key}. Expected string or list. Skipping.")
    return valid_entries

def modify_metadata(file_path, new_metadata):
    valid_entries = validate_metadata_input(new_metadata)
    if not valid_entries:
        logger.error("No valid metadata to update.")
        return None

    try:
        flac = FLAC(file_path)
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return None
    except FLACNoHeaderError:
        logger.error(f"Invalid FLAC file: {file_path}")
        return None
    except Exception as e:
        logger.exception(f"Unexpected error opening {file_path}: {e}")
        return None

    flac.update(valid_entries)

    try:
        flac.save()
        return True
    except Exception as e:
        logger.exception(f"Error saving changes to {file_path}: {e}")
        return None

def get_user_metadata_changes(current_metadata):
    updated_metadata = {}
    print("\nEnter new values for the fields you want to modify (press Enter to skip):")
    
    predefined_fields = ['TITLE', 'ARTIST', 'ALBUM', 'DATE', 'GENRE']
    for field in predefined_fields:
        current_value = current_metadata.get(field, [''])[0]
        new_value = input(f"Current {field}: {current_value}\nNew {field} (Enter to skip): ").strip()
        if new_value:
            updated_metadata[field] = new_value
    
    while True:
        new_field = input("Enter a new metadata field name (or press Enter to finish): ").strip()
        if not new_field:
            break
        new_value = input(f"Enter value for {new_field}: ").strip()
        if new_value:
            updated_metadata[new_field] = new_value
    
    return updated_metadata

def main():
    parser = argparse.ArgumentParser(description='FLAC metadata reader and editor')
    parser.add_argument('file_path', help='Path to the FLAC file')
    args = parser.parse_args()

    while True:
        action = input("\nDo you want to (v)iew or (m)odify metadata? (v/m): ").lower()
        if action in ['v', 'm']:
            break
        print("Please enter 'v' for view or 'm' for modify.")

    metadata = read_metadata(args.file_path)
    
    if action == 'v':
        print_metadata(metadata)
    
    elif action == 'm':
        if metadata is None:
            print("Cannot modify metadata: Error reading file")
            sys.exit(1)
            
        print_metadata(metadata)
        new_metadata = get_user_metadata_changes(metadata)
        
        if new_metadata:
            print("\nProposed changes:")
            print("-" * 40)
            for key, value in new_metadata.items():
                print(f"{key}: {value}")
            print("-" * 40)
            
            confirm = input("\nDo you want to save these changes? (y/n): ").lower()
            if confirm == 'y':
                if modify_metadata(args.file_path, new_metadata):
                    print("\nChanges saved successfully!")
                    print("\nUpdated metadata:")
                    print_metadata(read_metadata(args.file_path))
                else:
                    print("Error saving changes.")
            else:
                print("Changes discarded.")
        else:
            print("No changes were made.")
    
    sys.exit()

if __name__ == "__main__":
    main()