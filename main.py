from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq
import os
import json
from dotenv import load_dotenv # <-- ADD THIS

load_dotenv() # <-- ADD THIS: It loads the key from the .env file

app = FastAPI()
client = Groq() # Groq will automatically find the key now!

# ... the rest of your code remains exactly the same ...






# Initialize the Groq client. It will automatically look for the GROQ_API_KEY environment variable.
client = Groq()

# Define the data structure we expect from Flutter
class StudyMaterialRequest(BaseModel):
    text_content: str

@app.post("/generate")
async def generate_materials(request: StudyMaterialRequest):
    if not request.text_content:
        raise HTTPException(status_code=400, detail="Text content is required")

    system_prompt = """
    You are an expert educational assistant. Analyze the provided text and generate study materials.
    You must return a strictly valid JSON object with two keys:
    1. 'flashcards': an array of objects, each with 'front' (the question/concept) and 'back' (the answer).
    2. 'quiz': an array of objects, each with 'question', 'options' (array of 4 strings), and 'correct_answer' (the exact string of the correct option).
    """

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": request.text_content}
            ],
            model="llama3-70b-8192",
            response_format={"type": "json_object"},
            temperature=0.3
        )

        # Parse the JSON string returned by Groq into a Python dictionary
        result = json.loads(chat_completion.choices[0].message.content)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"status": "Backend is running!"}