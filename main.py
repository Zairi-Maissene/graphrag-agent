from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict
import os
import re
import json
import subprocess
from services.agents.agent import Agent
from services.lancedb_retriever import retrieve_docs
from services.llm.llm import LLMClient
import uvicorn

app = FastAPI(
    title="Document Processing API",
    description="API for uploading PDFs, retrieving information, and querying with natural language.",
    version="1.0.0"
)

# Define response models
class UploadResponse(BaseModel):
    document_id: str = Field(..., description="Unique ID of the uploaded document.")

class RetrieveResultItem(BaseModel):
    text: str = Field(..., description="Text content from the document.")
    distance: float = Field(..., description="Distance metric for the retrieved text chunk.")

class RetrieveResponse(BaseModel):
    result: List[RetrieveResultItem] = Field(..., description="List of results with text and score.")

class AnswerResponse(BaseModel):
    answer: str = Field(..., description="The agent's response.")

# Request models
class PDFUploadRequest(BaseModel):
    url: str = Field(..., example="https://example.com/document.pdf", description="URL of the PDF to upload.")

@app.post("/upload", response_model=UploadResponse, summary="Upload PDF", response_description="Document ID of the uploaded PDF")
async def upload_pdf(request: PDFUploadRequest):
    """
    Uploads a PDF file from the given URL and returns a unique document ID.
    """
    return {"document_id": document_id}


class RetrieveRequest(BaseModel):
    document_id: str = Field(..., example="12345", description="Unique ID of the document.")
    query: str = Field(..., example="What is the summary of chapter 1?", description="Query to search in the document.")

@app.get("/retrieve", response_model=RetrieveResponse, summary="Retrieve information from document", response_description="Response to the query")
def retrieve(request: RetrieveRequest):
    """
    Retrieves information from a specific document based on the provided query.
    """
    try:
        response = retrieve_docs(request.document_id, request.query)
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while processing the query.")
    return {"result": response}


class AnswerRequest(BaseModel):
    document_id: str = Field(..., example="12345", description="Unique ID of the document.")
    query: str = Field(..., example="Explain the conclusion of the document.", description="Query to ask the document.")

@app.get("/answer", response_model=AnswerResponse, summary="Query the document with natural language", response_description="Response from the agent")
async def chat_with_document(request: AnswerRequest):
    """
    Sends a natural language query to an AI agent for the specified document.
    """
    document_id = request.document_id
    query = request.query
    try:
        agent = Agent()
        response = agent(document_id, query)
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while processing the query.")
    return {"answer": response}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
