import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def ask_llm(prompt:str):
    payload={
        "model":"llama3",
        "prompt":prompt,
        "stream": False
    }
    response=requests.post(OLLAMA_URL,json=payload)
    return response.json()["response"]