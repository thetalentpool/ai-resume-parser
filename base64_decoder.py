import json
import logging
import os
from base64 import b64decode
from datetime import datetime
import argparse

# Set up argument parsing
parser = argparse.ArgumentParser(description='Decode Base64 encoded data from a JSON file')
parser.add_argument('--write-all', action='store_true', help='Write all files regardless of existence')
parser.add_argument('--write-new', action='store_true', help='Write only new files that do not already exist')
args = parser.parse_args()

# Get the current date and time
current_time = datetime.now()
log_directory = 'logs'
log_filename = f'decoding_logs_{current_time.strftime("%Y_%m_%d_%H_%M_%S")}.log'
log_file_path = os.path.join(log_directory, log_filename)

# Ensure 'logs' directory exists or create it
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Configure logging to save to the dynamically named log file
logging.basicConfig(level=logging.INFO, filename=log_file_path,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Directory to save the files
output_directory = 'output_files'

# Create the directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Read data from input.json
with open('exported_dataset_1189933_1190932.json') as json_file:
    data = json.load(json_file)

# Function to determine file type based on magic numbers
def determine_file_type(bytes_data):
    if bytes_data[0:4] == b'%PDF':
        return 'pdf'
    elif bytes_data[0:2] == b'\xFF\xD8':
        return 'jpg'
    elif bytes_data[0:4] == b'\x50\x4B\x03\x04':
        return 'docx'
    elif bytes_data[0:8] == b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A':
        return 'png'
    elif bytes_data[0:8] == b'\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1':
        return 'doc'
    elif bytes_data[0:4] == b'SP01':
        return 'bin'
    else:
        return 'bin'  # Treat any unsupported file type as a bin file

# Iterate over each item in the JSON data
for item in data:
    id = item['id']
    api_request = item['api_request']
    b64_string = api_request.encode('utf-8')

    # Decode the Base64 string
    try:
        bytes_data = b64decode(b64_string, validate=True)
    except Exception as e:
        logging.error(f'Error decoding Base64 string for id: {id} - {e}')
        continue

    # Determine file type based on magic number
    file_type = determine_file_type(bytes_data)

    # If file type is None, it's unsupported
    if file_type is None:
        logging.warning(f'Unsupported file format for id: {id}')
        continue

    # Determine output file path
    output_file_path = os.path.join(output_directory, f'file_{id}.{file_type}')

    # Check if the file exists
    if os.path.exists(output_file_path):
        if args.write_all:
            logging.info(f'Overwriting existing file for id: {id}')
        elif args.write_new:
            logging.info(f'Skipping existing file for id: {id}')
            continue
        else:
            logging.info(f'File already exists for id: {id}')
            continue
    else:
        logging.info(f'Writing new file for id: {id}')

    # Write the file contents to a local file in the output directory
    with open(output_file_path, 'wb') as f:
        f.write(bytes_data)

# Logging completed
logging.info('Decoding completed!')

