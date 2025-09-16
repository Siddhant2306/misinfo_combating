# Main functions
import json
import re
import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv

# Helper functions
from ai_client.gemini import Gemini
from services.fast_check import search_claims

last_response = None
app = FastAPI()

def load_system_prompt():
    try:
        with open("src/prompts/base_prompt.md", "r") as f:
            return f.read()
    except FileNotFoundError:
        return None

# Loads the API key from .env
load_dotenv()
system_prompt = load_system_prompt()
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set.")

ai_platform = Gemini(api_key=gemini_api_key, system_prompt=system_prompt)

# Pydantic models
class ChatRequest(BaseModel):
    prompt: str

class ChatResponse(BaseModel):
    response: str
    fact_sources: list

@app.get("/")
def root():
    return {"message": "API is working"}

@app.post("/chat")
def chat_request(request: ChatRequest):
    global last_response

    clean_prompt = str(request.prompt).strip()
    print(f"Clean prompt: {clean_prompt}")
    print(f"your type :" ,type(clean_prompt))

    try:
        claims_output = search_claims(clean_prompt)
    except Exception as e:
        print(f"Error in fact checking: {e}")
        print(f"Your prompt: {clean_prompt}", "Type:", type(clean_prompt))
        claims_output = []

    context = f"User asked: {request.prompt}\n\n"
    if claims_output:
        context += "Fact check sources suggest the following:\n"
        for c in claims_output:
            context += f"- {c['text']}\n"
            for review in c["claimReview"]:
                context += f"  Rating: {review['textualRating']} (Source: {review['publisher']['name']}, {review['url']})\n"
    else:
        context += "No fact-check sources found. Please analyze reliability."

    response_text = ai_platform.chat(context)
    last_response = response_text

    return {
        "claims": claims_output,
        "gemini_analysis": response_text
    }

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
