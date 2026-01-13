import os
import requests

def transcribe_whisper_api(audio_file):
    # Retrieve token from environment variables
    hf_token = os.getenv("HF_API_TOKEN")
    if not hf_token:
        print("HF_API_TOKEN not found in environment variables.")
        return "Error: HF_API_TOKEN not found."

    API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"
    headers = {"Authorization": f"Bearer {hf_token}"}

    # Audio file is a BytesIO object, read its content
    data = audio_file.read()
    # Reset pointer if needed, though read() usually consumes it
    audio_file.seek(0)

    response = requests.post(API_URL, headers=headers, data=data)
    
    if response.status_code == 200:
        return response.json().get("text", "")
    else:
        print(f"Whisper API Error: {response.status_code} - {response.text}")
        return f"Error: Transcription failed ({response.status_code})"
