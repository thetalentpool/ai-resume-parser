# Base64 Decoding Script

This script decodes Base64 encoded data from a JSON file and writes the decoded files to a specified directory. It also logs the operations performed, including any errors encountered.

## Features

- Decodes Base64 encoded data from a JSON file.
- Determines file type based on magic numbers.
- Writes files to an output directory.
- Supports command-line arguments to control file writing behavior.
- Logs operations and errors to a dynamically named log file.

## Requirements

- Python 3.x

## Files

- `exported_dataset_1189933_1190932.json` - Input JSON file containing Base64 encoded data.
- `output_files/` - Directory where decoded files are saved.
- `logs/` - Directory where log files are stored.

## Usage

### Command-Line Arguments

- `--write-all`: Write all files, even if they already exist. This option will overwrite existing files.
- `--write-new`: Write only new files that do not already exist. This option will skip files that are already present.

### Example Commands

1. **Write all files:**

    ```bash
    python base64_decoder.py --write-all
    ```

2. **Write only new files:**

    ```bash
    python base64_decoder.py --write-new
    ```

3. **Default behavior (skip existing files):**

    ```bash
    python base64_decoder.py
    ```

## How It Works

1. The script parses command-line arguments.
2. Creates necessary directories for logs and output files if they don't exist.
3. Reads Base64 encoded data from `exported_dataset_1189933_1190932.json`.
4. Decodes the Base64 strings and determines the file type based on the magic numbers.
5. Writes the decoded data to files in the `output_files/` directory.
6. Logs the operations and any errors encountered during the process.

## File Type Detection

The script identifies the following file types based on magic numbers:

- **PDF** (`%PDF`)
- **JPEG** (`\xFF\xD8`)
- **DOCX** (`\x50\x4B\x03\x04`)
- **PNG** (`\x89\x50\x4E\x47\x0D\x0A\x1A\x0A`)
- **DOC** (`\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1`)
- **Binary** (default for unsupported types)

## Logging

Logs are stored in the `logs/` directory with filenames that include the timestamp of execution. The log level is set to `INFO` by default.

## Example JSON Format

```json
[
    {
        "id": "1",
        "api_request": "Base64EncodedStringHere"
    },
    {
        "id": "2",
        "api_request": "AnotherBase64EncodedStringHere"
    }
]
```


# File Processing and Text Extraction Script

This script processes PDF, DOCX, and image files to extract text and save the extracted information in JSON format. It utilizes various libraries and tools for text extraction and integrates with OpenAI's GPT model for advanced information extraction.

## Features

- Processes PDF, DOCX, and image files.
- Uses OCR to extract text from image-based PDFs.
- Integrates with OpenAI's GPT model to extract information from text.
- Supports command-line arguments to control file writing behavior.
- Logs operations and errors to a dynamically named log file.

## Requirements

- Python 3.x
- `requests`
- `langchain_community`
- `pytesseract`
- `PIL` (Pillow)
- `pdfplumber`
- `config` module (custom)
- Tesseract OCR executable

## Installation

Install the required Python packages using pip:

```bash
pip install requests langchain_community pytesseract Pillow pdfplumber
```

## Configuration

    OpenAI API Key: Set your OpenAI API key in the config.py file.
    Tesseract Path: Update the path to the Tesseract executable in the script if you are using Windows.

## Files and Directories

    ouput_files/: Directory containing the input files (PDF, DOCX, and images).
    logs/: Directory where log files are stored.
    config.py: Configuration file containing system_prompt, user_prompt, json_template, and OPENAI_API_KEY

## Usage
Command-Line Arguments

    --write-all: Overwrite all files, even if they already exist.
    --write-new: Write only new files that do not already exist.

## Example Commands
1.Overwrite all files:
```bash
python resume_parser.py --write-all
```

2. Write only new files:

```bash
python resume_parser.py --write-new
```

3. Default behavior (skip existing files):

```bash
python resume_parser.py
```

## How It Works
1. Setup: Creates necessary directories for logs and output files. Configures logging.
2. File Processing: Lists all PDF, DOCX, and image files in the input directory.
3. Text Extraction:
        For PDFs: Extracts text using PyPDFLoader. Falls back to OCR if the text is empty.
        For DOCX files: Extracts text using Docx2txtLoader.
        For Images: Extracts text using Tesseract OCR.
   
4. Information Extraction: Sends extracted text to OpenAI's GPT model for further information extraction.

5. File Writing: Saves extracted information to JSON files in the extracted_json directory.

6. Logging: Records operations and errors to a log file.

# Document and File Conversion Script

This script performs two main tasks:
1. Converts `.doc` files to `.docx` format.
2. Renames `.bin` files to `.pdf` format.

The script includes logging functionality to track operations and errors.

## Features

- Converts `.doc` files to `.docx` using Microsoft Word COM automation.
- Renames `.bin` files to `.pdf`.
- Logs operations and errors to a dynamically named log file.

## Requirements

- Python 3.x
- `pywin32` (for COM automation with Microsoft Word)
- Microsoft Word installed on the system (required for `.doc` to `.docx` conversion)

## Installation

Install the required Python package using pip:

```bash
pip install pywin32
```
## Running the Script
```bash
python doc_to_docx_and_bin_to_pdf.py
```
