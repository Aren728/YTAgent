import os
from dotenv import load_dotenv

load_dotenv() # This loads the .env file automatically

# Replace the hardcoded keys with this:
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

import os
from dotenv import load_dotenv

load_dotenv() # This loads the .env file automatically

# Replace the hardcoded keys with this:
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")


import os
import requests
import subprocess
import asyncio
import edge_tts
from groq import Groq

# --- CONFIGURATION ---
GROQ_API_KEY = "GROQ_API_KEY"
PEXELS_API_KEY = "PEXELS_API_KEY"

NICHE = "Mind Blowing Facts"
VOICE_ID = "en-US-GuyNeural" # Let's use a bold male voice this time!

# --- AGENT 1: SCRIPT WRITER (Groq) ---
def generate_script():
    print("📝 1. AI Script Writer: Working...")
    client = Groq(api_key=GROQ_API_KEY)
    # Prompted to write short, punchy sentences for better captions
    prompt = f"Write a 30-second YouTube Short script about {NICHE}. Use exactly 5 to 7 short sentences. No filler words."
    chat = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="llama-3.3-70b-versatile")
    return chat.choices[0].message.content.replace('\n', ' ')

# --- AGENT 2: PRO VOICE (Edge TTS) ---
def generate_pro_voice(text, filename="audio.mp3"):
    print("🎙️ 2. Pro Voice Agent: Generating neural audio...")
    async def _generate():
        communicate = edge_tts.Communicate(text, VOICE_ID) 
        await communicate.save(filename)
    asyncio.run(_generate())
    return filename

# --- AGENT 3: MOTION BACKGROUNDS (Pexels) ---
def get_motion_background(query, filename="bg.mp4"):
    print("🎥 3. Visual Agent: Fetching vertical motion video...")
    headers = {"Authorization": PEXELS_API_KEY}
    url = f"https://api.pexels.com/videos/search?query={query}&orientation=portrait&per_page=1"
    response = requests.get(url, headers=headers).json()
    
    if 'videos' in response and len(response['videos']) > 0:
        video_files = response['videos'][0]['video_files']
        # Find an HD vertical video
        video_url = next((vf['link'] for vf in video_files if vf['height'] == 1920), video_files[0]['link'])
        
        img_data = requests.get(video_url, stream=True).content
        with open(filename, 'wb') as handler:
            handler.write(img_data)
        print("✅ HD Motion video downloaded!")
    else:
        print("⚠️ No video found, using fallback black screen.")
        # Fallback
        subprocess.run(['ffmpeg', '-y', '-f', 'lavfi', '-i', 'color=c=black:s=1080x1920:d=10', '-c:v', 'libx264', filename])
    return filename

# --- AGENT 4: HORMOZI-STYLE CAPTIONS & VIDEO ASSEMBLER ---
def create_viral_video(audio_file, video_file, script, output_file="final_viral_short.mp4"):
    print("🎨 4. Video Agent: Burning animated captions...")
    
    # 1. Get audio duration
    cmd = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {audio_file}'
    duration = float(subprocess.check_output(cmd, shell=True).decode().strip())
    
    # 2. Split script into 2-3 word chunks for fast-paced captions
    words = script.split()
    chunks = [' '.join(words[i:i+3]) for i in range(0, len(words), 3)]
    
    # 3. Generate an .ass (Advanced SubStation Alpha) subtitle file for animations
    chunk_duration = duration / len(chunks)
    
    with open("captions.ass", "w", encoding="utf-8") as f:
        f.write("[Script Info]\nPlayResX: 1080\nPlayResY: 1920\n\n")
        f.write("[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n")
        # Yellow text (&H0000FFFF), Black outline, Bold, Center Middle (Alignment 5)
        f.write("Style: Default,Arial,64,&H0000FFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,4,2,5,10,10,10,1\n\n")
        f.write("[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
        
        for i, chunk in enumerate(chunks):
            start = i * chunk_duration
            end = (i + 1) * chunk_duration
            
            # Format time for ASS (H:MM:SS.CC)
            def format_time(t):
                h = int(t // 3600)
                m = int((t % 3600) // 60)
                s = int(t % 60)
                c = int((t * 100) % 100)
                return f"{h}:{m:02d}:{s:02d}.{c:02d}"
            
            # \fad(100,100) creates a quick pop-in animation
            f.write(f"Dialogue: 0,{format_time(start)},{format_time(end)},Default,,0,0,0,,{{\\fad(100,100)}}\\b1{chunk.upper()}\n")

    # 4. Combine Video + Audio + Subtitles using FFmpeg
    # We use the 'subtitles' filter to burn the .ass file onto the video
    command = [
        'ffmpeg', '-y', '-i', video_file, '-i', audio_file,
        '-vf', "subtitles=captions.ass:force_style='FontName=Arial Bold'",
        '-c:v', 'libx264', '-c:a', 'aac', '-t', str(duration), '-shortest',
        '-preset', 'fast', output_file
    ]
    subprocess.run(command)
    print("✅ Viral video assembled!")
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
        "snippet": {"title": title, "description": description, "tags": ["AI", "Shorts", "Facts"], "categoryId": "22"},
        "status": {"privacyStatus": "private"}
    }
    media = MediaFileUpload(video_file, chunksize=-1, resumable=True)
    request = youtube.videos().insert(part=",".join(body.keys()), body=body, media_body=media)
    response = request.execute()
    print(f"✅ SUCCESS! Video ID: {response['id']}")

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    print(" VIRAL YOUTUBE SHORTS AGENT STARTING...")
    
    # 1. Script
    script = generate_script()
    print(f"📝 Script: {script}")
    
    # 2. Audio
    audio_file = generate_pro_voice(script)
    
    # 3. Motion Background (Search using the first word of the niche)
    bg_video = get_motion_background(NICHE.split()[0])
    
    # 4. Assemble with Captions
    video_file = create_viral_video(audio_file, bg_video, script)
    
    # 5. Publish
    upload_to_youtube(video_file, f"{NICHE} #Shorts", script)