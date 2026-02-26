from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from llm import ask_llm
from tools import get_weather

app = FastAPI()

class Prompt(BaseModel):
    prompt: str

@app.post("/chat")
def chat(data: Prompt):
    user_prompt = data.prompt

    # 1️⃣ Ask LLM if weather is needed
    intent_prompt = (
        "Answer only yes or no.\n"
        f"Does this question need real-time weather data?\n"
        f"Question: {user_prompt}"
    )

    intent = ask_llm(intent_prompt)

    # 2️⃣ If weather is needed
    if "yes" in intent.lower():
        # simple city extraction (enough for project)
        city = user_prompt.split()[-1].replace("?", "").replace(".", "")


        weather = get_weather(city)
        if not weather:
            raise HTTPException(status_code=400, detail="Invalid city name")

        final_prompt = (
            f"Weather data:\n"
            f"Temperature: {weather['temperature']}°C\n"
            f"Condition: {weather['condition']}\n"
            f"Explain this in simple English."
        )

        answer = ask_llm(final_prompt)

    # 3️⃣ If weather not needed
    else:
        answer = ask_llm(user_prompt)

    return {
        "answer": answer.strip()
    }
