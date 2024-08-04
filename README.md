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
