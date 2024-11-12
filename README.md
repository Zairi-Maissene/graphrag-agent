# GraphRag Search API

This project is a FastAPI-based API for querying data within a graph-based search system. It provides endpoints for uploading PDFs, retrieving data from a graph, and answering questions based on the content of a document.

## Table of Contents
1. [Setup](#setup)
2. [Usage](#usage)
    - [Upload PDF](#upload-pdf)
    - [Retrieve Data](#retrieve-data)
    - [Answer Question](#answer-question)



## Setup

### Prerequisites

1. **Python 3.10+** is required.
2. **Virtual environment** (optional but recommended).



### Installation Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/Zairi-Maissene/graphrag-agent
   cd graphrag-agent
    ```
2. Create a virtual environment (optional):

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```
   ```bash
    pip install --upgrade docling
    ```
   (Install docling seperately due to conflicting dependencies) 
   
4. Set the environment variables:

   ```bash
   GRAPHRAG_API_KEY = "your-api-key"
   ```
   You can also change the llm and embedding models

5. Run the application:
   ```bash
    uvicorn main:app 
    ```
   
6. The application should now be running on `http://localhost:8000`.

7. You can access the API documentation at `http://localhost:8000/docs`.


## Usage

### Upload PDF
This will create a graph representation of the document and return a `document_id`, this could take a while for large files.
```bash
Example:
curl -X POST http://localhost:8000/upload \
     -H "Content-Type: application/json" \
     -d '{"url": "https://arxiv.org/pdf/2408.09869"}'
```
### Retrieve Data
Use the returned `document_id` to retrieve data from the graph created for that document.
```bash
Example:
curl -X GET http://localhost:8000/retrieve \
        -H "Content-Type: application/json" \
        -d '{"document_id": "your-document-id", "query": "What is Docling?"}'
    
```
### Ask Questions

Use the `document_id` to ask questions based on the content of the document.
```bash
Example:
curl -X GET http://localhost:8000/answer \
        -H "Content-Type: application/json" \
        -d '{"document_id": "your-document-id", "question": "What is Docling?"}'
```


