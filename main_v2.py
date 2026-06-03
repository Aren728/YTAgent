import os
from dotenv import load_dotenv

load_dotenv() # This loads the .env file automatically

# Replace the hardcoded keys with this:
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

import os
import requests
import subprocess
from groq import Groq

try:
   import asyncio
   import edge_tts
except ImportError:
    class ElevenLabs:
        def __init__(self, *args, **kwargs):
            raise RuntimeError("elevenlabs package is not installed. Install with `pip install elevenlabs` to use text-to-speech.")

    def save(*args, **kwargs):
        raise RuntimeError("elevenlabs package is not installed. Install with `pip install elevenlabs` to use text-to-speech.")

# --- CONFIGURATION ---
GROQ_API_KEY = "os.getenv("GROQ_API_KEY")"
ELEVENLABS_API_KEY = "Eleven_Key"
UNSPLASH_ACCESS_KEY = "-ElPEXELS_API_KEPEXELS_API_KE"

NICHE = "Space Facts"
VOICE_ID = "21m00Tcm4TlvDq8ikWAM" # Standard ElevenLabs "Rachel" Voice

# --- AGENT 1: SCRIPT WRITER (Groq) ---
def generate_script():
    print("📝 1. AI Script Writer: Working...")
    client = Groq(api_key=GROQ_API_KEY)
    prompt = f"Write a 30-second engaging YouTube Short about {NICHE}. 4 short sentences max. No scene directions."
    chat = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="llama-3.3-70b-versatile")
    return chat.choices[0].message.content

# --- AGENT 2: PRO VOICE (Microsoft Edge Neural TTS - 100% Free) ---
def generate_pro_voice(text, filename="audio.mp3"):
    print("🎙️ 2. Pro Voice Agent: Generating neural audio...")
    
    # We use an async wrapper because edge-tts is asynchronous
    async def _generate():
        # "en-US-AriaNeural" is a highly popular, natural-sounding female voice
        # You can also use "en-US-GuyNeural" for a male voice
        communicate = edge_tts.Communicate(text, "en-US-AriaNeural") 
        await communicate.save(filename)

    # Run the async function
    asyncio.run(_generate())
    
    print("✅ Audio generated successfully!")
    return filename

# --- AGENT 3: HD VISUALS (Unsplash) ---
def get_background_image(query, filename="background.jpg"):
    print("️ 3. Visual Agent: Fetching HD background...")
    url = f"https://api.unsplash.com/search/photos?query={query}&per_page=1&client_id={UNSPLASH_ACCESS_KEY}"
    response = requests.get(url).json()
    img_url = response['results'][0]['urls']['regular']
    
    # Download the image
    img_data = requests.get(img_url).content
    with open(filename, 'wb') as handler:
        handler.write(img_data)
    return filename

# --- AGENT 4: VIDEO ASSEMBLER & CAPTIONS (FFmpeg) ---
def create_video_with_captions(audio_file, image_file, script, output_file="final_pro_short.mp4"):
    print("🎨 4. Video Agent: Assembling video and burning captions...")
    
    # 1. Get audio duration
    cmd = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {audio_file}'
    duration = float(subprocess.check_output(cmd, shell=True).decode().strip())
    
    # 2. Split script into caption lines (roughly 1 sentence per 3 seconds)
    lines = script.replace('\n', ' ').split('.')
    lines = [l.strip() for l in lines if len(l.strip()) > 5]
    
    # 3. Create a simple subtitle file (.srt)
    with open("captions.srt", "w") as f:
        start_time = 0
        chunk_time = duration / len(lines)
        for i, line in enumerate(lines):
            end_time = start_time + chunk_time
            f.write(f"{i+1}\n")
            f.write(f"00:00:{int(start_time):02d},000 --> 00:00:{int(end_time):02d},000\n")
            f.write(f"{line.strip()}\n\n")
            start_time = end_time

    # 4. Burn captions and combine using FFmpeg
    # Note: Using a standard Windows font path
    font_path = "C\\:/Windows/Fonts/arial.ttf".replace("\\", "/")
    
    command = [
        'ffmpeg', '-y', '-loop', '1', '-i', image_file,
        '-i', audio_file,
        '-vf', f"scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,subtitles=captions.srt:force_style='FontSize=24,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,Outline=2,Alignment=10'",
        '-c:v', 'libx264', '-c:a', 'aac', '-t', str(duration), '-shortest',
        output_file
    ]
    subprocess.run(command)
    return output_file

# --- AGENT 5: PUBLISHING ENGINE (YouTube) ---
def upload_to_youtube(video_file, title, description):
    print("🚀 5. Publishing Agent: Uploading to YouTube...")
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload

    scopes = ["https://www.googleapis.com/auth/youtube.upload"]
    flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", scopes)
    credentials = flow.run_local_server(port=0)
    youtube = build("youtube", "v3", credentials=credentials)

    body = {
        "snippet": {"title": title, "description": description, "tags": ["AI", "Shorts"], "categoryId": "22"},
        "status": {"privacyStatus": "private"}
    }
    media = MediaFileUpload(video_file, chunksize=-1, resumable=True)
    request = youtube.videos().insert(part=",".join(body.keys()), body=body, media_body=media)
    response = request.execute()
    print(f"✅ SUCCESS! Video ID: {response['id']}")

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    print("🤖 ULTIMATE YOUTUBE AUTOMATION AGENT STARTING...")
    
    # 1. Strategy
    script = generate_script()
    print(f"Script: {script}")
    
    # 2. Audio
    audio_file = generate_pro_voice(script)
    
    # 3. Visuals (Search for the first word of the niche, e.g., "Space")
    bg_image = get_background_image(NICHE.split()[0])
    
    # 4. Video & Captions
    video_file = create_video_with_captions(audio_file, bg_image, script)
    
    # 5. Publish
    upload_to_youtube(video_file, f"{NICHE} Shorts", script)