import os
import google.generativeai as genai
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import subprocess

# --- CONFIGURATION ---
GEMINI_API_KEY = "Key"
NICHE = "Space Facts" # Change this to your niche
VIDEO_TITLE = "Did You Know? Space Edition"

import random

from groq import Groq
import os

# --- AGENT 1: SCRIPT WRITER (Groq AI - Fast & Free) ---
def generate_script():
    print("📝 Script Writer Agent: Working (Powered by Groq)...")
    
    # Paste your Groq key here (starts with gsk_)
    GROQ_API_KEY = "KEY" 
    
    client = Groq(api_key=GROQ_API_KEY)
    
    prompt = f"""
    Write a 45-second engaging YouTube Short script about {NICHE}. 
    Structure:
    1. A viral hook in the first 3 seconds.
    2. Three interesting and mind-blowing facts.
    3. A strong call to action at the end.
    Keep sentences short and punchy. Do not include scene directions.
    """
    
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile", # A highly intelligent, free model
    )
    
    return chat_completion.choices[0].message.content
    
    prompt = f"""
    Write a 45-second YouTube Short script about {NICHE}. 
    Structure:
    1. A viral hook in the first 3 seconds.
    2. Three interesting facts.
    3. A strong call to action at the end.
    Keep sentences short and punchy.
    """
    response = model.generate_content(prompt)
    return response.text

# --- AGENT 2: VOICEOVER ENGINE (Local Coqui TTS) ---
def generate_voice(text, filename="voiceover.wav"):
    print("🎙️ Voiceover Agent: Generating audio...")
    try:
        from TTS.api import TTS
        tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=False)
        tts.tts_to_file(text=text, file_path=filename)
        return filename
    except Exception as e:
        print(f"TTS Error: {e}. Switching to basic system voice.")
        # Fallback to simple system voice if Coqui fails
        import pyttsx3
        engine = pyttsx3.init()
        engine.save_to_file(text, filename)
        engine.runAndWait()
        return filename

# --- AGENT 3: VIDEO ASSEMBLER (FFmpeg) ---
def create_video(audio_file, output_file="final_short.mp4"):
    print("🎨 Thumbnail & Video Agent: Assembling video...")
    # For now, we create a black screen with audio. 
    # Later, we can add images or Stable Diffusion generations here.
    command = [
        'ffmpeg', '-y', '-f', 'lavfi', '-i', 'color=c=black:s=1080x1920:d=10',
        '-i', audio_file,
        '-c:v', 'libx264', '-c:a', 'aac', '-shortest',
        output_file
    ]
    subprocess.run(command)
    return output_file

# --- AGENT 4: PUBLISHING ENGINE (YouTube API) ---
def upload_to_youtube(video_file, title, description):
    print("🚀 Publishing Agent: Uploading to YouTube...")
    
    # This handles the OAuth flow automatically!
    scopes = ["https://www.googleapis.com/auth/youtube.upload"]
    flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", scopes)
    credentials = flow.run_local_server(port=0)
    
    youtube = build("youtube", "v3", credentials=credentials)
    
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": ["Shorts", "AI", "Facts"],
            "categoryId": "22" # People & Blogs
        },
        "status": {
            "privacyStatus": "private" # Safe start!
        }
    }
    
    media = MediaFileUpload(video_file, chunksize=-1, resumable=True)
    request = youtube.videos().insert(part=",".join(body.keys()), body=body, media_body=media)
    response = request.execute()
    
    print(f"✅ SUCCESS! Video ID: {response['id']}")

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    print("🤖 YouTube Automation Agent Starting...")
    
    # 1. Strategy & Script
    script = generate_script()
    print(f"Script Preview: {script[:100]}...")
    
    # 2. Audio Generation
    audio_file = generate_voice(script)
    
    # 3. Video Assembly
    video_file = create_video(audio_file)
    
    # 4. Publishing
    upload_to_youtube(video_file, VIDEO_TITLE, script)