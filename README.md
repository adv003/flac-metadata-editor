# FLAC Metadata Editor

#### Video Demo:  [Your Video URL Here]

## Description:
The FLAC Metadata Editor is a Python-based tool designed to read, modify, and save metadata in FLAC audio files. The project was developed as part of the CS50P course and demonstrates how to work with file metadata using the `mutagen` library, while also showcasing robust error handling, logging, and testing with `pytest`.

## Project Structure:
- **project.py:**  
  Contains the main function and all the core functions:
    - `main()`: Entry point for the command-line interface.
    - `read_metadata(file_path)`: Reads metadata from a FLAC file with robust error handling.
    - `modify_metadata(file_path, new_metadata)`: Modifies and saves metadata with input validation and logging.
    
- **test_project.py:**  
  Contains unit tests for all the custom functions. Each function has a corresponding test (prefixed with `test_`) to ensure it behaves as expected, even under error conditions.
    
- **requirements.txt:**  
  Lists all pip-installable libraries required by the project (e.g., `mutagen`, `pytest`).
    
- **README.md:**  
  This file, which explains the project, its functionalities, design decisions, and how to run the code.
    
- **samples/**  
  Contains sample FLAC files used for testing and demonstration.

## Key Features:
- **Metadata Reading:**  
  The project uses `mutagen` to extract metadata such as artist, title, and album from FLAC files.
  
- **Metadata Modification:**  
  Users can update metadata fields via the command-line interface or by directly invoking functions. Input validation ensures only valid data is written.
  
- **Robust Error Handling:**  
  The application handles various error scenarios such as file not found, invalid file format, and unexpected issues, logging errors for easier debugging.
  
- **Unit Testing:**  
  Comprehensive tests have been written using `pytest` to ensure that both normal operation and error conditions are handled correctly.

## Design Choices:
- **Error Handling & Logging:**  
  By implementing detailed error handling and logging, the application provides meaningful feedback in the event of an error, improving the user experience and maintainability.
    
- **Modular Structure:**  
  All functionality is contained in `project.py` and tested via `test_project.py`, keeping the project structure simple and organized.
    
- **Command-Line Interface:**  
  A CLI was implemented (using `argparse`) to allow users to easily interact with the project, specifying file paths and metadata changes directly from the terminal.

## How to Run the Project:
1. **Install Dependencies:**  
   Run `pip install -r requirements.txt` to install all necessary libraries.
    
2. **Run the Project:**  
   Execute `python project.py` in your terminal. The CLI will provide instructions for reading or modifying metadata.
    
3. **Run Tests:**  
   Use `pytest test_project.py` to run the automated tests and ensure everything is working as expected.

## Final Thoughts:
This project was built as part of the CS50P course, demonstrating the use of Python for practical file manipulation and error handling. The thorough testing and logging practices implemented here reflect industry standards, ensuring a robust and user-friendly application.

---
