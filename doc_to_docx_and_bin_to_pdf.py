import os
import pythoncom
from win32com import client
import logging
from datetime import datetime

# Set up logging
logs_directory = "logs"
if not os.path.exists(logs_directory):
    os.makedirs(logs_directory)

log_file = datetime.now().strftime("conversion_log_%Y-%m-%d_%H-%M-%S.log")
log_path = os.path.join(logs_directory, log_file)
logging.basicConfig(filename=log_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def convert_doc_to_docx(doc_path, docx_path):
    try:
        pythoncom.CoInitialize()
        word = client.Dispatch("Word.Application")
        doc = word.Documents.Open(doc_path)
        doc.SaveAs(docx_path, FileFormat=16)  # 16 is the format for .docx
        doc.Close()
        word.Quit()
        # Delete the original .doc file after conversion
        os.remove(doc_path)
        logging.info(f'Converted {doc_path} to {docx_path}')
    except Exception as e:
        logging.error(f'Error converting {doc_path} to {docx_path}: {e}')

def rename_bin_to_pdf(bin_path, pdf_path):
    try:
        os.rename(bin_path, pdf_path)
        logging.info(f'Renamed {bin_path} to {pdf_path}')
    except Exception as e:
        logging.error(f'Error renaming {bin_path} to {pdf_path}: {e}')

def convert_files_in_directory(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if filename.endswith('.doc'):
                docx_path = os.path.splitext(file_path)[0] + '.docx'
                convert_doc_to_docx(file_path, docx_path)
            elif filename.endswith('.bin'):
                pdf_path = os.path.splitext(file_path)[0] + '.pdf'
                rename_bin_to_pdf(file_path, pdf_path)
        except Exception as e:
            logging.error(f'Error processing file {file_path}: {e}')

# Example usage
directory_path = "C:/Users/AmitKumarManjhi/Documents/Projects/Resume_Parser_Project/output_files/"
convert_files_in_directory(directory_path)

