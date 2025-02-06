import os
import logging
import requests
import pdfplumber
import base64
import openai
import time
from PIL import Image
from io import BytesIO
import fitz  # PyMuPDF
import io
import subprocess
from zipfile import ZipFile
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
import platform

if platform.system() == "Windows":
    try:
        from win32com.client import Dispatch
    except ImportError:
        print("pywin32 is not installed. Install it using: pip install pywin32")

class OpenAIClient:
    def __init__(self, api_key):
        start_time = time.time()
        if api_key is None:
            raise ValueError("OpenAI API key is not set.")
        self.api_key = api_key
        self.client = openai.Client(api_key=self.api_key)
        logging.info(f"Initialized OpenAIClient in {time.time() - start_time:.2f} seconds.")


    def extract_resume_info(self, system_prompt, user_prompt, json_template, resume_text):
        start_time = time.time()
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"{user_prompt}\n{json_template}\n{resume_text}\nPlease respond in valid JSON format according to the given template."}
            ]
        }

        response = requests.post(url, headers=headers, json=data, verify=False)
        logging.info(f"Extracted resume info in {time.time() - start_time:.2f} seconds.")
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            logging.error(f"Error extracting resume info: {response.status_code}, {response.text}")
            return None


    def call_gpt4o(self, base64_image, user_prompt, json_template,system_prompt):
        start_time = time.time()
        response = self.client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"{user_prompt}\n{json_template}\nPlease respond in valid JSON format according to the given template."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]
            }
        ],
        max_tokens=4096

    )
        logging.info(f"Called GPT-4o in {time.time() - start_time:.2f} seconds.")
        return response.choices[0].message.content

# File Processor Class
class FileProcessor:
    def __init__(self, input_directory, output_directory, client, args, system_prompt, user_prompt, json_template):
        start_time = time.time()
        self.input_directory = input_directory
        self.output_directory = output_directory
        self.client = client
        self.args = args
        self.system_prompt = system_prompt
        self.user_prompt = user_prompt
        self.json_template = json_template
        logging.info(f"Initialized FileProcessor in {time.time() - start_time:.2f} seconds.")

    # PDF to images conversion
    def convert_pdf_to_images(self, pdf_path):
        start_time = time.time()
        images = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                try:
                    images.append(page.to_image(resolution=300).original)
                except Exception as e:
                    logging.error(f"Error extracting image from PDF page: {str(e)}")
        logging.info(f"Converted PDF to images in {time.time() - start_time:.2f} seconds.")
        return images

    # Image encoding
    def encode_image_to_base64(self, image_path):
        start_time = time.time()
        try:
            with open(image_path, "rb") as image_file:
                logging.info(f"Encoded image to base64 in {time.time() - start_time:.2f} seconds.")
                return base64.b64encode(image_file.read()).decode("utf-8")
        except Exception as e:
            logging.error(f"Error encoding image to base64: {str(e)}")
            return None

    # File processing function for images
    def process_image_file(self, image_file_path,json_template):
        start_time = time.time()
        try:
            if not os.path.exists(image_file_path):
                logging.error(f"Image file not found: {image_file_path}")
                return None

            base64_image = self.encode_image_to_base64(image_file_path)
            if base64_image:
                extracted_text = self.client.call_gpt4o(base64_image, "Extract text from this image",json_template,self.system_prompt)
                logging.info(f"Processed image file in {time.time() - start_time:.2f} seconds.")
                return extracted_text
            else:
                logging.error(f"Failed to encode image: {image_file_path}")
                return None
        except Exception as e:
            logging.error(f"Error processing image file {image_file_path}: {str(e)}")
            return None

    def write_output_file(self, filename, extracted_text):
        """Writes extracted text to a JSON file, handling --write-all and --write-new flags."""
        start_time = time.time()
        
        # Construct output file path
        output_filename = os.path.splitext(filename)[0] + "_extracted_info.json"
        output_filepath = os.path.join(self.output_directory, output_filename)

        # Check if file exists
        file_exists = os.path.exists(output_filepath)

        # Handle --write-all and --write-new flags
        if file_exists and not self.args.write_all:
            if self.args.write_new:
                logging.info(f"Skipping existing file: {output_filepath}")
                return None  # Skip processing if file already exists and --write-new is set
            else:
                logging.info(f"File already exists: {output_filepath}")
                return output_filepath  # Return existing file path

        # Write extracted text to JSON file
        try:
            with open(output_filepath, "w", encoding="utf-8") as json_file:
                #json.dump(extracted_text, f, ensure_ascii=False, indent=4)
                 json_file.write(extracted_text)
                 json_file.write("\n")
            logging.info(f"Successfully written to: {output_filepath}")
        except Exception as e:
            logging.error(f"Failed to write file {output_filepath}: {e}")
            return None

        end_time = time.time()
        logging.info(f"Time taken to write file: {end_time - start_time:.2f} seconds")

        return output_filepath

    # Process PDF files
    def process_pdf_files(self, pdf_files):

        for pdf_file in pdf_files:
            start_time = time.time()
            pdf_file_path = os.path.join(self.input_directory, pdf_file)

            try:
                pdf_loader = PyPDFLoader(pdf_file_path)
                pdf_text = "".join(page.page_content for page in pdf_loader.load())

                # Check if extracted text is empty
                if not pdf_text.strip():
                    logging.warning(f"Empty text extracted from {pdf_file}, processing images instead.,")
                    combined_image_path = self.extract_and_combine_images(pdf_file_path)
                    
                    # Process combined image
                    if combined_image_path and os.path.exists(combined_image_path):
                        base64_image = self.encode_image_to_base64(combined_image_path)
                        pdf_text = self.client.call_gpt4o(base64_image, "Extract text from this combined image",self.json_template,self.system_prompt)

                resume_info = self.client.extract_resume_info(
                    self.system_prompt, 
                    self.user_prompt, 
                    self.json_template, 
                    pdf_text
                )

                self.write_output_file(pdf_file, resume_info)
                logging.info(f"Processed PDF file {pdf_file} in {time.time() - start_time:.2f} seconds.")

                #processed_files.add(pdf_file)
            except Exception as e:
                logging.error(f"Error processing PDF {pdf_file}: {str(e)}")

    # Process DOCX files
    def process_docx_files(self, docx_files):
        for docx_file in docx_files:
            start_time = time.time()
            docx_file_path = os.path.join(self.input_directory, docx_file)
            try:
                docx_loader = Docx2txtLoader(docx_file_path)
                docx_text = "".join(page.page_content for page in docx_loader.load())

                if not docx_text.strip():
                    logging.warning(f"Empty text extracted from {docx_file}, processing images instead.")
                    combined_image_path = self.extract_and_combine_images_from_docx(docx_file_path)

                    # Process combined image if it exists
                    if combined_image_path and os.path.exists(combined_image_path):
                        base64_image = self.encode_image_to_base64(combined_image_path)
                        docx_text = self.client.call_gpt4o(base64_image, "Extract text from this combined image",self.json_template,self.system_prompt)

                resume_info = self.client.extract_resume_info(
                    self.system_prompt, 
                    self.user_prompt, 
                    self.json_template, 
                    docx_text
                )

                self.write_output_file(docx_file, resume_info)
                logging.info(f"Processed DOCX file {docx_file} in {time.time() - start_time:.2f} seconds.")

            except Exception as e:
                logging.error(f"Error processing DOCX {docx_file}: {str(e)}")

    # Process Image files
    def process_image_files(self, image_files):
        for image_file in image_files:
            start_time = time.time()
            image_file_path = os.path.join(self.input_directory, image_file)
            extracted_info = self.process_image_file(image_file_path, self.json_template)  # No separate call to extract_resume_info
            if extracted_info:
                self.write_output_file(image_file, extracted_info)
                logging.info(f"Processed image file {image_file} in {time.time() - start_time:.2f} seconds.")



    def extract_and_combine_images(self, pdf_path):
        start_time = time.time()
        # Extract the base name of the PDF (without extension)
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        input_dir = os.path.dirname(pdf_path)  # Directory where the PDF is located
        output_path = os.path.join(input_dir, f"{base_name}.jpg")

        if os.path.exists(output_path):
            logging.info(f"Combined image already exists for {pdf_path}: {output_path}")
            return output_path  # Return the path of the existing combined image
        
        # Open the PDF
        pdf = fitz.open(pdf_path)
        all_images = []  # List to store extracted images

        for page_number in range(len(pdf)):
            page = pdf[page_number]
            images = page.get_images(full=True)

            for img_index, img in enumerate(images):
                xref = img[0]
                base_image = pdf.extract_image(xref)
                image_bytes = base_image["image"]

                # Convert image bytes to PIL Image object
                image = Image.open(io.BytesIO(image_bytes))
                all_images.append(image)

        # Combine all images into one
        if all_images:
            # Determine the size of the combined image
            widths, heights = zip(*(img.size for img in all_images))
            total_width = max(widths)
            total_height = sum(heights)

            # Create a blank canvas
            combined_image = Image.new("RGB", (total_width, total_height))

            # Paste images on the canvas
            y_offset = 0
            for img in all_images:
                combined_image.paste(img, (0, y_offset))
                y_offset += img.height

            # Save the combined image in the same directory as the input PDF
            output_path = os.path.join(input_dir, f"{base_name}.jpg")
            combined_image.save(output_path)
            print(f"Combined image saved at: {output_path}")
            logging.info(f"Extracted and combined images from PDF in {time.time() - start_time:.2f} seconds.")
            return output_path  # Return the path of the combined image
        else:
            print(f"No images found in {pdf_path}.")
            return None

    def extract_and_combine_images_from_docx(self, docx_path):
        # Extract the base name of the DOCX (without extension)
        start_time = time.time()
        base_name = os.path.splitext(os.path.basename(docx_path))[0]
        input_dir = os.path.dirname(docx_path)  # Directory where the DOCX is located
        output_path = os.path.join(input_dir, f"{base_name}.jpg")
        
        # Check if combined image already exists
        if os.path.exists(output_path):
            logging.info(f"Combined image already exists for {docx_path}: {output_path}")
            return output_path  # Return the path of the existing combined image

        # Open the DOCX file as a zip archive
        with ZipFile(docx_path, 'r') as docx_zip:
            image_files = [f for f in docx_zip.namelist() if f.startswith('word/media/')]
            
            # Extract all images
            all_images = []
            for image_file in image_files:
                image_data = docx_zip.read(image_file)
                image = Image.open(BytesIO(image_data))
                all_images.append(image)

        # Combine all images into one
        if all_images:
            # Determine the size of the combined image
            widths, heights = zip(*(img.size for img in all_images))
            total_width = max(widths)
            total_height = sum(heights)

            # Create a blank canvas
            combined_image = Image.new("RGB", (total_width, total_height))

            # Paste images on the canvas
            y_offset = 0
            for img in all_images:
                combined_image.paste(img, (0, y_offset))
                y_offset += img.height

            # Save the combined image in the same directory as the input DOCX
            combined_image.save(output_path)
            logging.info(f"Combined image saved at: {output_path}")
            logging.info(f"Extracted and combined images from DOCX in {time.time() - start_time:.2f} seconds.")

            return output_path  # Return the path of the combined image
        else:
            logging.warning(f"No images found in {docx_path}.")
            return None
        

    def convert_doc_to_docx(self,doc_path):
        """ Convert a .doc file to .docx using MS Word (Windows) or LibreOffice (Linux/Mac). """
        if not os.path.exists(doc_path):
            print(f"ERROR: File not found: {doc_path}")
            return None

        docx_path = doc_path.replace(".doc", ".docx")

        if os.name == "nt":  # Windows
            try:
                print(f" Converting {doc_path} to {docx_path} using MS Word...")
                word = Dispatch("Word.Application")
                word.Visible = False  # Background execution
                doc = word.Documents.Open(os.path.abspath(doc_path))
                doc.SaveAs(os.path.abspath(docx_path), FileFormat=16)  # Convert to .docx
                doc.Close()
                word.Quit()
                print(f"Conversion successful: {docx_path}")
                return docx_path
            except Exception as e:
                print(f"ERROR: Failed to convert {doc_path} - {e}")
                return None
            
        elif os.name == "posix":  # Linux/macOS
            try:
                print(f" Converting {doc_path} using LibreOffice...")
                subprocess.run(["libreoffice", "--headless", "--convert-to", "docx", doc_path], check=True)
                return docx_path if os.path.exists(docx_path) else None
            except Exception as e:
                print(f"ERROR: LibreOffice conversion failed for {doc_path} - {e}")
                return None
        else:
            print(f"Unsupported OS: {os.name}")


        
    def process_doc_files(self, doc_files):
        for doc_file in doc_files:
            start_time = time.time()
            doc_file_path = os.path.join(self.input_directory, doc_file)

            # Convert .doc to .docx
            docx_file_path = self.convert_doc_to_docx(doc_file_path)
            if not docx_file_path:
                logging.error(f"Skipping {doc_file} due to conversion failure.")
                continue  # Skip processing if conversion fails

            try:
                # Process converted .docx file
                docx_loader = Docx2txtLoader(docx_file_path)
                doc_text = "".join(page.page_content for page in docx_loader.load())

                if not doc_text.strip():
                    logging.warning(f"Empty text extracted from {doc_file}, processing images instead.")
                    combined_image_path = self.extract_and_combine_images_from_docx(docx_file_path)

                    # Process extracted images
                    if combined_image_path and os.path.exists(combined_image_path):
                        base64_image = self.encode_image_to_base64(combined_image_path)
                        doc_text = self.client.call_gpt4o(base64_image, "Extract text from this combined image", self.json_template,self.system_prompt)

                resume_info = self.client.extract_resume_info(
                    self.system_prompt, self.user_prompt, self.json_template, doc_text
                )

                self.write_output_file(doc_file, resume_info)
                logging.info(f"Processed DOC file {doc_file} in {time.time() - start_time:.2f} seconds.")

            except Exception as e:
                logging.error(f"Error processing DOC {doc_file}: {str(e)}")
    