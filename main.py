import os
import argparse
from utils.functions import OpenAIClient, FileProcessor
from log_helper import setup_logging
from config import system_prompt, user_prompt, json_template, OPENAI_API_KEY

# Set up logging
setup_logging()

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Process files and extract text.')
    parser.add_argument('--write-all', action='store_true', help='Overwrite all files')
    parser.add_argument('--write-new', action='store_true', help='Skips already processed files.')
    parser.add_argument('--process', type=str, help='Process a single file (provide file name with extension)')
    
    args = parser.parse_args()

    # Define input and output directories
    input_directory = "input_files"
    output_directory = "extracted_json"

    # Ensure output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Initialize OpenAI Client
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

    # Process a single file if --process argument is given
    if args.process:
        file_path = os.path.join(input_directory, args.process)
        if not os.path.exists(file_path):
            print(f"ERROR: File '{args.process}' not found in '{input_directory}'")
            return
        
        # Determine file type and process accordingly
        if args.process.endswith('.pdf'):
            file_processor.process_pdf_files([args.process])
        elif args.process.endswith('.docx'):
            file_processor.process_docx_files([args.process])
        elif args.process.lower().endswith(('.jpg', '.jpeg', '.png')):
            file_processor.process_image_files([args.process])
        elif args.process.lower().endswith('.doc'):
            file_processor.process_doc_files([args.process])
        else:
            print(f"ERROR: Unsupported file type '{args.process}'")
        return  # Exit after processing single file

    # Get list of files from the input directory (if --process is not used)
    pdf_files = [f for f in os.listdir(input_directory) if f.endswith('.pdf')]
    docx_files = [f for f in os.listdir(input_directory) if f.endswith('.docx')]
    image_files = [f for f in os.listdir(input_directory) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    doc_files = [f for f in os.listdir(input_directory) if f.lower().endswith('.doc')]

    # Process all files
    file_processor.process_pdf_files(pdf_files)
    file_processor.process_docx_files(docx_files)
    file_processor.process_image_files(image_files)
    file_processor.process_doc_files(doc_files)

if __name__ == "__main__":
    main()

