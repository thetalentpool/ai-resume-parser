import os
import json
import logging
from datetime import datetime
import requests
import argparse
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from config import system_prompt, user_prompt, json_template, OPENAI_API_KEY
import pytesseract
from PIL import Image
import pdfplumber


# Specify the path to the Tesseract executable (for Windows, update this path if necessary)
pytesseract.pytesseract.tesseract_cmd = r'C:/Users/AmitKumarManjhi/AppData/Local/Programs/Tesseract-OCR/tesseract.exe' 

# Create logs directory if it doesn't exist
logs_directory = "logs"
if not os.path.exists(logs_directory):
    os.makedirs(logs_directory)

# Set up logging
log_file = datetime.now().strftime("parser_log_%Y-%m-%d_%H-%M-%S.log")
log_path = os.path.join(logs_directory, log_file)
logging.basicConfig(filename=log_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up argument parsing
parser = argparse.ArgumentParser(description='Process files, extract text, and save extracted information to JSON files.')
parser.add_argument('--write-all', action='store_true', help='Overwrite all files regardless of their existence')
parser.add_argument('--write-new', action='store_true', help='Write only files that do not already exist')
args = parser.parse_args()


def extract_resume_info(system_prompt, user_prompt, json_template, resume_text):
    if OPENAI_API_KEY is None:
        raise ValueError("OpenAI API key is not set in environment variables.")

    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": f"{user_prompt}\n{json_template}\n{resume_text}"
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    # Check if the request was successful
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        print("Error:", response.status_code, response.text)

def convert_pdf_to_images(pdf_path):
    images = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            try:
                image = page.to_image(resolution=300).original
                images.append(image)
            except Exception as e:
                logging.error(f"Error extracting image from PDF page: {str(e)}")
    return images

def extract_text_with_pytesseract(images):
    image_content = []
    for image in images:
        raw_text = pytesseract.image_to_string(image)
        image_content.append(raw_text)
    return "\n".join(image_content)

def extract_text_from_image(image):
    return pytesseract.image_to_string(image)

# Directory containing the files
input_directory = "output_files"  
output_directory = "extracted_json"  

# Create the output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# List all PDF and DOCX files in the input directory
pdf_files = [f for f in os.listdir(input_directory) if f.endswith('.pdf') or f.endswith('.bin')]
docx_files = [f for f in os.listdir(input_directory) if f.endswith('.docx') or f.endswith('.doc')]
image_files = [f for f in os.listdir(input_directory) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

# Initialize counters
pdf_count = 0
docx_count = 0
image_count = 0

# Process PDF files
for pdf_file in pdf_files:
    pdf_file_path = os.path.join(input_directory, pdf_file)
    try:
        # Try extracting text normally
        pdf_loader = PyPDFLoader(pdf_file_path)
        pdf_text = "".join(page.page_content for page in pdf_loader.load())
        
        # If normal extraction fails, extract images and apply OCR
        if not pdf_text.strip():
            logging.warning(f"Fallback to OCR for {pdf_file}: Extracted text is empty, likely an image-based PDF")
            images = convert_pdf_to_images(pdf_file_path)
            pdf_text = extract_text_with_pytesseract(images)
        
        extracted_info_pdf = extract_resume_info(system_prompt, user_prompt, json_template, pdf_text)
        output_filename = os.path.splitext(pdf_file)[0] + "_extracted_info.json"
        output_filepath = os.path.join(output_directory, output_filename)

        # Check if the file exists
        if os.path.exists(output_filepath):
            if args.write_all:
                logging.info(f'Overwriting existing file for PDF: {pdf_file}')
            elif args.write_new:
                logging.info(f'Skipping existing file for PDF: {pdf_file}')
                continue
            else:
                logging.info(f'File already exists for PDF: {pdf_file}')
                continue
        else:
            logging.info(f'Writing new file for PDF: {pdf_file}')

        with open(output_filepath, "w") as json_file:
            json.dump(extracted_info_pdf, json_file)
        pdf_count += 1
        logging.info(f"Successfully extracted information from PDF file: {pdf_file}")
    except Exception as e:
        logging.error(f"Error processing PDF file {pdf_file}: {str(e)}")

# Process DOCX files
for docx_file in docx_files:
    docx_file_path = os.path.join(input_directory, docx_file)
    try:
        docx_loader = Docx2txtLoader(docx_file_path)
        docx_text = "".join(page.page_content for page in docx_loader.load())
        extracted_info_docx = extract_resume_info(system_prompt, user_prompt, json_template, docx_text)
        output_filename = os.path.splitext(docx_file)[0] + "_extracted_info.json"
        output_filepath = os.path.join(output_directory, output_filename)

        # Check if the file exists
        if os.path.exists(output_filepath):
            if args.write_all:
                logging.info(f'Overwriting existing file for DOCX: {docx_file}')
            elif args.write_new:
                logging.info(f'Skipping existing file for DOCX: {docx_file}')
                continue
            else:
                logging.info(f'File already exists for DOCX: {docx_file}')
                continue
        else:
            logging.info(f'Writing new file for DOCX: {docx_file}')

        with open(output_filepath, "w") as json_file:
            json.dump(extracted_info_docx, json_file)
        docx_count += 1
        logging.info(f"Successfully extracted information from DOCX file: {docx_file}")
    except Exception as e:
        logging.error(f"Error processing DOCX file {docx_file}: {str(e)}")

# Process image files
for image_file in image_files:
    image_file_path = os.path.join(input_directory, image_file)
    try:
        image_text = extract_text_from_image(Image.open(image_file_path))
        extracted_info_image = extract_resume_info(system_prompt, user_prompt, json_template, image_text)
        output_filename = os.path.splitext(image_file)[0] + "_extracted_info.json"
        output_filepath = os.path.join(output_directory, output_filename)

        # Check if the file exists
        if os.path.exists(output_filepath):
            if args.write_all:
                logging.info(f'Overwriting existing file for image: {image_file}')
            elif args.write_new:
                logging.info(f'Skipping existing file for image: {image_file}')
                continue
            else:
                logging.info(f'File already exists for image: {image_file}')
                continue
        else:
            logging.info(f'Writing new file for image: {image_file}')

        with open(output_filepath, "w") as json_file:
            json.dump(extracted_info_image, json_file)
        image_count += 1
        logging.info(f"Successfully extracted information from image file: {image_file}")
    except Exception as e:
        logging.error(f"Error processing image file {image_file}: {str(e)}")

# Log count of processed files
logging.info(f"Processed {pdf_count} PDF files, {docx_count} DOCX files, and {image_count} image files.")
