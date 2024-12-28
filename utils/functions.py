import os
import json
import logging
import requests
import pdfplumber
import base64
import openai
from PIL import Image
from io import BytesIO
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader


class OpenAIClient:
    def __init__(self, api_key):
        if api_key is None:
            raise ValueError("OpenAI API key is not set.")
        self.api_key = api_key
        self.client = openai.Client(api_key=self.api_key)

    def extract_resume_info(self, system_prompt, user_prompt, json_template, resume_text):
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        data = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"{user_prompt}\n{json_template}\n{resume_text}\nPlease respond in valid JSON format according to the given template."}
            ]
        }

        response = requests.post(url, headers=headers, json=data, verify=False)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            logging.error(f"Error extracting resume info: {response.status_code}, {response.text}")
            return None

    def call_gpt4o(self, base64_image, question):
        
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": question},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                    ]
                }
            ],
            max_tokens=300,
        )
        return response.choices[0].message.content

# File Processor Class
class FileProcessor:
    def __init__(self, input_directory, output_directory, client, args, system_prompt, user_prompt, json_template):
        self.input_directory = input_directory
        self.output_directory = output_directory
        self.client = client
        self.args = args
        self.system_prompt = system_prompt
        self.user_prompt = user_prompt
        self.json_template = json_template

    # PDF to images conversion
    def convert_pdf_to_images(self, pdf_path):
        images = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                try:
                    images.append(page.to_image(resolution=300).original)
                except Exception as e:
                    logging.error(f"Error extracting image from PDF page: {str(e)}")
        return images

    # Image encoding
    def encode_image_to_base64(self, image_path):
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode("utf-8")
        except Exception as e:
            logging.error(f"Error encoding image to base64: {str(e)}")
            return None

    # File processing function for images
    def process_image_file(self, image_file_path):
        try:
            if not os.path.exists(image_file_path):
                logging.error(f"Image file not found: {image_file_path}")
                return None

            base64_image = self.encode_image_to_base64(image_file_path)
            if base64_image:
                extracted_text = self.client.call_gpt4o(base64_image, "Extract text from this image")
                return extracted_text
            else:
                logging.error(f"Failed to encode image: {image_file_path}")
                return None
        except Exception as e:
            logging.error(f"Error processing image file {image_file_path}: {str(e)}")
            return None

    # Write output to file
    def write_output_file(self, filename, extracted_text):
        output_filename = os.path.splitext(filename)[0] + "_extracted_info.json"
        output_filepath = os.path.join(self.output_directory, output_filename)
        if os.path.exists(output_filepath) and not self.args.write_all:
            logging.info(f"File already exists: {output_filepath}")
            return
        with open(output_filepath, "w") as json_file:
            json_file.write(extracted_text)
            json_file.write("\n")

        logging.info(f"Successfully extracted information from {filename}")

    # Process PDF files
    def process_pdf_files(self, pdf_files):
        for pdf_file in pdf_files:
            pdf_file_path = os.path.join(self.input_directory, pdf_file)
            try:
                pdf_loader = PyPDFLoader(pdf_file_path)
                pdf_text = "".join(page.page_content for page in pdf_loader.load())
                if not pdf_text.strip():
                    logging.warning(f"Fallback to GPT-4 for {pdf_file}: Empty extracted text.")
                    images = self.convert_pdf_to_images(pdf_file_path)
                    for image in images:
                        base64_image = self.encode_image_to_base64(image)
                        pdf_text += self.client.call_gpt4o(base64_image, "Extract text from this image")

                resume_info = self.client.extract_resume_info(
                    self.system_prompt, 
                    self.user_prompt, 
                    self.json_template, 
                    pdf_text
                )

                self.write_output_file(pdf_file, resume_info)
            except Exception as e:
                logging.error(f"Error processing PDF {pdf_file}: {str(e)}")

    # Process DOCX files
    def process_docx_files(self, docx_files):
        for docx_file in docx_files:
            docx_file_path = os.path.join(self.input_directory, docx_file)
            try:
                docx_loader = Docx2txtLoader(docx_file_path)
                docx_text = "".join(page.page_content for page in docx_loader.load())

                resume_info = self.client.extract_resume_info(
                    self.system_prompt, 
                    self.user_prompt, 
                    self.json_template, 
                    docx_text
                )

                self.write_output_file(docx_file, resume_info)
            except Exception as e:
                logging.error(f"Error processing DOCX {docx_file}: {str(e)}")

    # Process Image files
    def process_image_files(self, image_files):
        for image_file in image_files:
            image_file_path = os.path.join(self.input_directory, image_file)
            extracted_text = self.process_image_file(image_file_path)
            if extracted_text:
                resume_info = self.client.extract_resume_info(
                    self.system_prompt, 
                    self.user_prompt, 
                    self.json_template, 
                    extracted_text
                )
                self.write_output_file(image_file, resume_info)

