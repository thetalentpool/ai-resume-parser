import os
import argparse
import multiprocessing
from utils.functions import OpenAIClient, FileProcessor
from log_helper import setup_logging,logging
from config import system_prompt, user_prompt, json_template, OPENAI_API_KEY, IMAGE_API_KEY,INPUT_DIRECTORY,OUTPUT_DIRECTORY,PROCESS_TIMEOUT

def run_main_logic(args):
    input_directory = INPUT_DIRECTORY
    output_directory = OUTPUT_DIRECTORY
    setup_logging()

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    client = OpenAIClient(OPENAI_API_KEY, IMAGE_API_KEY)

    file_processor = FileProcessor(
        input_directory, 
        output_directory, 
        client, 
        args, 
        system_prompt, 
        user_prompt, 
        json_template
    )

    if args.process:
        file_path = os.path.join(input_directory, args.process)
        if not os.path.exists(file_path):
            print(f"ERROR: File '{args.process}' not found in '{input_directory}'")
            return

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
        return

    pdf_files = [f for f in os.listdir(input_directory) if f.endswith('.pdf')]
    docx_files = [f for f in os.listdir(input_directory) if f.endswith('.docx')]
    image_files = [f for f in os.listdir(input_directory) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    doc_files = [f for f in os.listdir(input_directory) if f.lower().endswith('.doc')]

    file_processor.process_pdf_files(pdf_files)
    file_processor.process_docx_files(docx_files)
    file_processor.process_image_files(image_files)
    file_processor.process_doc_files(doc_files)

def main():
    setup_logging()
    parser = argparse.ArgumentParser(description='Process files and extract text.')
    parser.add_argument('--write-all', action='store_true', help='Overwrite all files')
    parser.add_argument('--write-new', action='store_true', help='Skips already processed files.')
    parser.add_argument('--process', type=str, help='Process a single file (provide file name with extension)')
    
    args = parser.parse_args()

    # Use multiprocessing to run with timeout
    p = multiprocessing.Process(target=run_main_logic, args=(args,))
    p.start()
    p.join(timeout=PROCESS_TIMEOUT)  # timeout in seconds

    if p.is_alive():
        print("Timeout reached. Terminating process....")

        p.terminate()
        p.join()

if __name__ == "__main__":
    main()
