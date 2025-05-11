from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from groq import Groq
import os
import json
from typing import Dict, Any, Optional
from dotenv import load_dotenv


load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

app = FastAPI()

# Load character data from JSON files
def load_character_data(filename: str) -> Dict[str, Any]:
    try:
        with open(f"app/c_data/{filename}.json", "r") as file:
            return json.load(file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading character data: {str(e)}")

# Define request model
class ChatRequest(BaseModel):
    question: str
    prompt: Optional[str] = None  # Optional additional roleplay prompt

# Generate system prompt
def generate_system_prompt(character_data: Dict[str, Any], user_prompt: Optional[str] = None) -> str:
    prompt = f"You are {character_data['name']}, a {character_data['age']}-year-old {character_data['gender']} from {character_data['location']}.\n\n"
    
    #  bio and personality
    prompt += f"BIO: {character_data['bio']}\n\n"
    prompt += f"PERSONALITY: {character_data['personality']}\n\n"
    
    #  speech patterns
    speech = character_data.get('speech_patterns', {})
    if speech:
        prompt += "SPEECH PATTERNS:\n"
        prompt += f"- Your speaking pace is {speech.get('pace', 'normal')}\n"
        prompt += f"- Your speaking volume is {speech.get('volume', 'moderate')}\n"
        
        if 'catchphrases' in speech and speech['catchphrases']:
            prompt += "- You often use these catchphrases: " + ", ".join([f'"{phrase}"' for phrase in speech['catchphrases']]) + "\n"
        
        if 'filler_words' in speech and speech['filler_words']:
            prompt += "- You frequently use these filler words: " + ", ".join([f'"{word}"' for word in speech['filler_words']]) + "\n"
    
    # quirks
    if 'quirks' in character_data and character_data['quirks']:
        prompt += "\nQUIRKS:\n"
        for quirk in character_data['quirks']:
            prompt += f"- {quirk}\n"
    
    # emotional responses
    emotional = character_data.get('emotional_responses', {})
    if emotional:
        prompt += "\nEMOTIONAL RESPONSES:\n"
        for emotion, response in emotional.items():
            prompt += f"- When {emotion}: {response}\n"
    
    # AI instructions
    if 'ai_instruction' in character_data:
        prompt += f"\nSPECIAL INSTRUCTIONS: {character_data['ai_instruction']}\n\n"
    
    # Add additional user prompt if provided
    if user_prompt:
        prompt += f"ADDITIONAL CONTEXT: {user_prompt}\n\n"
    
    # Add JSON response format instructions
    prompt += "RESPONSE FORMAT: Your responses should be in the first person, as if you are the character speaking directly. Always maintain your character's personality and speech patterns.\n"
    prompt += "Return your response in JSON format with the following structure: {\"character_name\": \"" + character_data['name'] + "\", \"response\": \"Your in-character response here\"}"
    
    return prompt

# Create endpoints for each character
@app.post("/chat-aakash")
async def chat_aakash(request: ChatRequest):
    aakash_data = load_character_data("aakash")
    system_prompt = generate_system_prompt(aakash_data, request.prompt)
    
    completion = client.chat.completions.create(
        model="mistral-saba-24b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": request.question},
        ],
        temperature=0.7,
        max_completion_tokens=1024,
        top_p=1,
        stream=False,
        response_format={"type": "json_object"}
    )

    return json.loads(completion.choices[0].message.content)

@app.post("/chat-ankit")
async def chat_ankit(request: ChatRequest):
    ankit_data = load_character_data("ankit")
    system_prompt = generate_system_prompt(ankit_data, request.prompt)
    
    completion = client.chat.completions.create(
        model="mistral-saba-24b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": request.question},
        ],
        temperature=0.8,
        max_completion_tokens=1024,
        top_p=1,
        stream=False,
        response_format={"type": "json_object"}
    )

    return json.loads(completion.choices[0].message.content)

@app.post("/chat-aman")
async def chat_aman(request: ChatRequest):
    aman_data = load_character_data("aman")
    system_prompt = generate_system_prompt(aman_data, request.prompt)
    
    completion = client.chat.completions.create(
        model="mistral-saba-24b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": request.question},
        ],
        temperature=0.9,
        max_completion_tokens=1024,
        top_p=1,
        stream=False,
        response_format={"type": "json_object"}
    )

    return json.loads(completion.choices[0].message.content)


