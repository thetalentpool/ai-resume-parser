import os
import argparse
from utils.functions import OpenAIClient,FileProcessor
from log_helper import setup_logging
from config import system_prompt, user_prompt, json_template,OPENAI_API_KEY

# import ssl
# import certifi

# ssl._create_default_https_context = ssl.create_default_context
# ssl._create_default_https_context().load_verify_locations(certifi.where())

# Set up logging
setup_logging()

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Process files and extract text.')
    parser.add_argument('--write-all', action='store_true', help='Overwrite all files')
    parser.add_argument('--write-new', action='store_true', help='Overwrite all files')
    args = parser.parse_args()

    # Define input and output directories
    input_directory = "input_files"
    output_directory = "extracted_json"
    
    # Ensure output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Initialize OpenAI Client
    #OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    client = OpenAIClient(OPENAI_API_KEY)

    # Initialize file processor with prompts
    file_processor = FileProcessor(
        input_directory, 
        output_directory, 
        client, 
        args, 
        system_prompt, 
        user_prompt, 
        json_template
    )

    # Get list of files from the input directory
    pdf_files = [f for f in os.listdir(input_directory) if f.endswith('.pdf')]
    docx_files = [f for f in os.listdir(input_directory) if f.endswith('.docx')]
    image_files = [f for f in os.listdir(input_directory) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

    # Process PDF, DOCX, and image files
    file_processor.process_pdf_files(pdf_files)
    file_processor.process_docx_files(docx_files)
    file_processor.process_image_files(image_files)

if __name__ == "__main__":
    main()
