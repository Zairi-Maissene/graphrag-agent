import os
import shutil
import subprocess
from fastapi import HTTPException
from docling.datamodel.base_models import InputFormat
from docling.document_converter import DocumentConverter
import uuid
import requests

MAX_FILE_SIZE = 1024 * 1024 * 20 # 20 MB

def load_pdf(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        if "application/pdf" not in response.headers.get("Content-Type", ""):
            raise HTTPException(status_code=400, detail="The provided URL does not point to a PDF file.")

        # Process the PDF content
        converter = DocumentConverter(allowed_formats =InputFormat.PDF)
        conv_result = converter.convert(url,max_file_size=MAX_FILE_SIZE)
        processed_text = conv_result.document.export_to_text()

    except requests.RequestException:
        raise HTTPException(status_code=400, detail="Could not fetch the PDF file. Please check the URL.")

    except HTTPException:
        raise HTTPException(status_code=400, detail="The provided URL does not point to a PDF file.")

    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while processing the PDF file.")

    if len(processed_text.strip()) < 100:
        raise HTTPException(status_code=400, detail="Insufficient content in PDF document.")

    document_id = str(uuid.uuid4())
    document_name = f'document{document_id}.txt'
    if not os.path.exists(f'graphs/{document_id}/input'):
        os.makedirs(f'graphs/{document_id}/input', exist_ok=True)

    text_path = os.path.join("graphs", document_id, 'input', document_name)

    with open(text_path, "w", encoding='utf-8') as f:
        f.write(processed_text)

    setup_graphrag(document_id)

    return document_id

def setup_graphrag(document_id):
    try:
        init_command = f'python -m graphrag init --root graphs/{document_id}'
        subprocess.run(init_command, shell=True, check=True)

        # Delete any .env file in the directory
        directory_path = os.path.join('graphs', document_id)
        env_file_path = os.path.join(directory_path, '.env')
        if os.path.exists(env_file_path):
            os.remove(env_file_path)

        # Copy the settings.yaml file to the directory
        source_yaml_path = os.path.join('settings.yaml')
        destination_folder = os.path.join('graphs', document_id)
        destination_yaml_path = os.path.join(destination_folder, 'settings.yaml')
        os.makedirs(destination_folder, exist_ok=True)
        shutil.copyfile(source_yaml_path, destination_yaml_path)

        index_command = f'python -m graphrag index --root graphs/{document_id}'
        subprocess.run(index_command, shell=True, check=True)

    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while creating the document graph.")