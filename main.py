import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import asyncio
from dotenv import load_dotenv

# OpenAI
from openai import OpenAI  

# Google Cloud
from googleapiclient.discovery import build
from google.cloud import storage
from google.cloud import aiplatform

app = FastAPI()

class ChatRequest(BaseModel):
    prompt: str

@app.get("/")
def root():
    return {"message": "API is working"}

@app.post("/chat")
def chat_request(request: ChatRequest):
    global last_response
    last_response = request.prompt 
    return {"response": last_response}

@app.get("/chat")
def chat_get():
    return {"last_response": last_response}