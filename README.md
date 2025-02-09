FLAC Metadata Editor
The FLAC Metadata Editor is a Python-based tool designed to read, modify, and save metadata in FLAC audio files. It uses the mutagen library for FLAC file handling and includes robust error handling, logging, and comprehensive testing using pytest.

Features
Read Metadata: Extract metadata from FLAC files, including artist, title, album, and more.

Modify Metadata: Update metadata fields with new values, ensuring input validation.

Error Handling: Gracefully handles file not found, invalid FLAC format, and unexpected errors.

Logging: Logs all operations and errors to both the console and a log file (flac_editor.log).

Testing: Includes unit tests for all core functionalities using pytest.

Installation
Clone the Repository:

bash
Copy
git clone https://github.com/yourusername/flac-metadata-editor.git
cd flac-metadata-editor
Set Up a Virtual Environment:

bash
Copy
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
Install Dependencies:

bash
Copy
pip install -r requirements.txt
Usage
Reading Metadata
To read metadata from a FLAC file, use the read_metadata function:

python
Copy
from project import read_metadata

metadata = read_metadata("samples/04. All Falls Down.flac")
if metadata:
    print(metadata)
Modifying Metadata
To update metadata in a FLAC file, use the modify_metadata function:

python
Copy
from project import modify_metadata

new_metadata = {
    "TITLE": "New Title",
    "ARTIST": "New Artist"
}
success = modify_metadata("samples/04. All Falls Down.flac", new_metadata)
if success:
    print("Metadata updated successfully!")
Running Tests
To run the unit tests, use the following command:

bash
Copy
pytest
Project Structure
Copy
project/
  ├── project.py               # Main script with core functionalities
  ├── test_project.py          # Unit tests for the project
  ├── requirements.txt         # List of dependencies
  ├── README.md                # This file
  └── samples/                 # Sample FLAC files for testing
       └── 04. All Falls Down.flac
Error Handling and Logging
File Not Found: Logs an error and returns None.

Invalid FLAC Format: Logs an error and returns None.

Unexpected Errors: Logs the exception with a stack trace and returns None.

Logs: All logs are saved to flac_editor.log and printed to the console.

Testing Details
File Not Found: Ensures read_metadata returns None and logs the error.

Invalid FLAC Format: Tests with non-FLAC or corrupted files.

Unexpected Errors: Simulates scenarios like file permission issues.

Valid File Operations: Tests reading and modifying metadata for valid files.

Future Work
Add command-line argument support using argparse.

Implement batch editing, metadata export/import, and GUI support.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Feel free to contribute to this project by opening issues or submitting pull requests!