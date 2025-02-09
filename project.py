import logging
from mutagen.flac import FLAC, FLACNoHeaderError

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('flac_editor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def main():
    pass

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