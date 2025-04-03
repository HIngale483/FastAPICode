!pip install fastapi uvicorn requests

from fastapi import FastAPI
from pydantic import BaseModel
import requests
import json
import uvicorn
import threading
import os

# FastAPI app initialization
app = FastAPI()

# Set your Azure OpenAI API key and endpoint
api_key = os.getenv("2REOt9aAX9oB5DvGFPDY9apS4sFbHXkf677fzBzD5hdEQfFdAgfWJQQJ99BDACYeBjFXJ3w3AAABACOGWaX0")
endpoint = os.getenv("https://mychatbotservice2025.openai.azure.com/")
model = "gpt-4"
api_version = "2025-01-01-preview"  # Example API version, change as necessary

def query_openai(prompt: str):
    url = f"{endpoint}/openai/deployments/{model}/chat/completions?api-version={api_version}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    # Chat-style request payload for GPT-4
    data = {
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 150
    }
    # Make API request to Azure OpenAI
    response = requests.post(url, headers=headers, data=json.dumps(data))
    # Check for errors in the response
    if response.status_code != 200:
        return {"error": f"Failed to get response from OpenAI API. Status code: {response.status_code}"}
    # Print the full response to understand its structure
    print("Response from OpenAI API:", response.json())
    return response.json()
# Pydantic model to handle incoming data
class ChatRequest(BaseModel):
    prompt: str
# FastAPI route to handle chat requests

@app.post("/chat/")
async def chat(request: ChatRequest):
    prompt = request.prompt
    openai_response = query_openai(prompt)
    # Return OpenAI's response or error message
    if 'error' in openai_response:
        return {"error": openai_response['error']}
    
    return {"response": openai_response['choices'][0]['message']['content']}
# Function to run the Uvicorn server
def run_uvicorn():
    uvicorn.run(app, host="127.0.0.1", port=8000)  # Use port 8002 if 8001 is unavailable
# Start Uvicorn server in a new thread
thread = threading.Thread(target=run_uvicorn)
thread.start()




import requests
# Test the FastAPI chat API on a different port (8002)
url = "http://127.0.0.1:8000/chat/"
# data = {"prompt": "Hello, how are you?"}
data = {"prompt": "What is the capital of France?"}
response = requests.post(url, json=data)
# Check if the response is valid and can be decoded as JSON
try:
    response_json = response.json()
    print(response_json)
except ValueError:
    print(f"Failed to decode JSON. Response text: {response.text}")




