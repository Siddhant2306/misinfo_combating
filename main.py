import json
import os
import re
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import requests
from dotenv import load_dotenv

# OpenAI
#from openai import OpenAI  

# Google Cloud
from googleapiclient.discovery import build
from google.cloud import storage
#from google.cloud import aiplatform

from ai_client.gemini import Gemini

last_response = None
app = FastAPI()

def load_system_prompt():
    try:
        with open("src/prompts/base_prompt.md", "r") as f:
            return f.read()
    except FileNotFoundError:
        return None

#Loads the api key in my environment variable
load_dotenv()

system_prompt = load_system_prompt()
gemini_api_key = os.getenv("GEMINI_API_KEY") #now i can read it in my .env file

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set.")


ai_platform = Gemini(api_key=gemini_api_key, system_prompt=system_prompt)


class ChatRequest(BaseModel):
    prompt: str

class ChatResponse(BaseModel):
    response: str


@app.get("/")
def root():
    return {"message": "API is working"}


@app.post("/chat", response_model=ChatResponse)
def chat_request(request: ChatRequest):
    
    response_text = ai_platform.chat(request.prompt)

    global last_response
    last_response = response_text 
    return {"response": request.prompt , "response_by_model" : {response_text}}


def clean_markdown(text: str) -> str:
    
    text = re.sub(r"#+\s*", "", text)

    text = re.sub(r"(\*\*|\*|__|_)", "", text)
  
    text = re.sub(r"[*\-]\s*", "", text)
    return text.strip()

@app.get("/chat")
def chat_get():
    global last_response

    if not last_response:
        return JSONResponse(content={"last_response": []})

  
    clean_text = clean_markdown(last_response)

   
    points = re.split(r"\n|\d+\.\s*", clean_text)
    points = [p.strip() for p in points if p.strip()]


    print("\n===== Chat Response =====")
    for p in points:
        print(f"- {p}")
    print("========================\n")

    return JSONResponse(content={"last_response": points})