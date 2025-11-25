from moviepy import *
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import textwrap
import os
import math

# --- CONFIGURATION FOR YOUTUBE ---
WIDTH = 1920  # Full HD
HEIGHT = 1080 # Full HD
FPS = 30      # Standard for YouTube
BG_COLOR = (5, 5, 10) # Dark Blue-Black (Cinematic)
ACCENT_COLOR = (0, 255, 128) # Neon Green (Safety/Tech)
TEXT_COLOR = (240, 240, 240)

# --- ASSETS CHECK ---
AUDIO_MAP = {
    "intro": "01_intro.mp3",
    "def": "02_definition.mp3",
    "anat": "03_anatomy.mp3",
    "proc": "04_process.mp3",
    "q1": "05_quiz1_q.mp3",
    "a1": "05_quiz1_a.mp3",
    "q2": "06_quiz2_q.mp3",
    "a2": "06_quiz2_a.mp3"
}

SFX_MAP = {
    "trans": "sfx_transition.mp3",
    "alert": "sfx_alert.mp3",
    "correct": "sfx_correct.mp3"
}

# --- GRAPHIC ENGINE ---
def create_base_img():
    img = Image.new('RGB', (WIDTH, HEIGHT), color=BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # Grid Background (Tech feel)
    for x in range(0, WIDTH, 100):
        draw.line([(x, 0), (x, HEIGHT)], fill=(20, 20, 30), width=1)
    for y in range(0, HEIGHT, 100):
        draw.line([(0, y), (WIDTH, y)], fill=(20, 20, 30), width=1)
        
    return img, draw

def create_slide_img(title, content, subtext=""):
    img, draw = create_base_img()
    
    try:
        font_title = ImageFont.truetype("Chakra.ttf", 100)
        font_body = ImageFont.truetype("Sarabun.ttf", 60)
        font_small = ImageFont.truetype("Sarabun.ttf", 35)
    except:
        print("Warning: Fonts not found. Using default.")
        font_title = ImageFont.load_default()
        font_body = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Header Bar
    draw.rectangle([(0, 0), (WIDTH, 150)], fill=(10, 20, 40))
    draw.line([(0, 150), (WIDTH, 150)], fill=ACCENT_COLOR, width=5)
    
    # Safe Zone Text (YouTube Overlay Safe)
    draw.text((80, 40), title, font=font_title, fill=ACCENT_COLOR)
    draw.text((WIDTH - 400, 60), "ACADEMIC ARCHIVE", font=font_small, fill=(100, 200, 200))

    # Content Body
    y = 300
    lines = content.split('\n')
    for line in lines:
        wrapped_lines = textwrap.wrap(line, width=55)
        for w_line in wrapped_lines:
            draw.text((100, y), w_line, font=font_body, fill=TEXT_COLOR)
            y += 85
        y += 30

    # Footer / Watermark (Safety)
    draw.line([(0, HEIGHT-80), (WIDTH, HEIGHT-80)], fill=(40, 40, 50), width=2)
    if subtext:
        draw.text((80, HEIGHT-60), subtext, font=font_small, fill=(150, 150, 150))
    
    # Privacy Disclaimer
    draw.text((WIDTH - 600, HEIGHT-60), "AI-GENERATED CONTENT | PRIVACY PROTECTED", font=font_small, fill=(80, 80, 80))

    return np.array(img)

# --- CLIP FACTORY ---
def make_clip(title, content, audio_key, sfx_key=None, duration_buffer=1.0, sub=""):
    print(f"Processing Scene: {title}...")
    
    img_array = create_slide_img(title, content, sub)
    
    voice_clip = None
    clip_duration = 5.0

    if audio_key and os.path.exists(AUDIO_MAP.get(audio_key, "")):
        voice_clip = AudioFileClip(AUDIO_MAP[audio_key])
        clip_duration = voice_clip.duration + duration_buffer
    
    # Create Video Clip
    clip = ImageClip(img_array).with_duration(clip_duration)
    
    # Audio Mixing
    audio_layers = []
    if voice_clip:
        audio_layers.append(voice_clip)
    
    if sfx_key and os.path.exists(SFX_MAP.get(sfx_key, "")):
        sfx = AudioFileClip(SFX_MAP[sfx_key]).with_volume_scaled(0.5)
        audio_layers.append(sfx)

    if audio_layers:
        final_audio = CompositeAudioClip(audio_layers)
        clip = clip.with_audio(final_audio)
        
    # Add Fade In/Out for Smoothness
    clip = clip.with_effects([vfx.CrossFadeIn(0.5)])

    return clip

# --- MAIN PRODUCTION ---
def main():
    print("\n=== YOUTUBE RENDER ENGINE STARTED ===")
    print("Target Resolution: 1920x1080 (1080p)")
    print("Privacy Mode: ENABLED\n")
    
    clips = []

    # 0. YouTube Intro (Black Screen Fade In)
    intro_black = ColorClip(size=(WIDTH, HEIGHT), color=(0,0,0), duration=2)
    clips.append(intro_black)

    # 1. Title Slide
    clips.append(make_clip(
        "การเขียนรายงานเชิงวิชาการ",
        "รายงานวิชาการ (Academic Report)\n\nผู้จัดทำ: นายพงศกร พ.\n(Student Project)", 
        "intro", "trans", 2.0, "Initiating Knowledge Base..."
    ))

    # 2. Definition
    clips.append(make_clip(
        "01. นิยาม (DEFINITION)",
        "• การศึกษาค้นคว้าอย่างมีระบบ (Systematic)\n• รวบรวมข้อมูลจากแหล่งที่เชื่อถือได้ (Facts)\n• วิเคราะห์และเรียบเรียงใหม่ (Synthesis)\n• เป้าหมาย: นำเสนอ 'ความจริง' (Truth)",
        "def", "trans", 1.5, "Module 1: Core Concept"
    ))

    # 3. Anatomy
    clips.append(make_clip(
        "02. องค์ประกอบ (ANATOMY)",
        "1. ส่วนนำ: ปก, คำนำ, สารบัญ\n2. ส่วนเนื้อหา: บทนำ, เนื้อเรื่อง, สรุป\n   (หัวใจสำคัญของรายงาน)\n3. ส่วนท้าย: บรรณานุกรม, ภาคผนวก",
        "anat", "trans", 1.5, "Module 2: Structure Analysis"
    ))

    # 4. Process
    clips.append(make_clip(
        "03. ขั้นตอนการทำ (PROCESS)",
        "1. เลือกหัวข้อ & กำหนดขอบเขต\n2. ค้นคว้าข้อมูล (Research)\n3. วางโครงเรื่อง (Outline)\n4. เรียบเรียง & อ้างอิง (Citation)\n5. ตรวจทาน (Review)",
        "proc", "trans", 1.5, "Module 3: Execution Flow"
    ))

    # 5. Quiz 1 Question
    clips.append(make_clip(
        "KNOWLEDGE CHECK: Q1",
        "\nส่วนประกอบใดของรายงาน...\nที่ทำหน้าที่ยืนยันความถูกต้อง และป้องกันการ\n'โจรกรรมทางปัญญา' (Plagiarism)?",
        "q1", "alert", 0.5, "Question 1: Evaluating..."
    ))

    # 5. Quiz 1 Answer
    clips.append(make_clip(
        "KNOWLEDGE CHECK: Q1",
        "\nคำตอบ:\n\n[ บรรณานุกรม ]\n(Bibliography & Citation)",
        "a1", "correct", 1.5, "Answer Verified"
    ))

    # 6. Quiz 2 Question
    clips.append(make_clip(
        "KNOWLEDGE CHECK: Q2",
        "\nภาษาที่ใช้เขียนรายงานเชิงวิชาการ...\nต้องเป็นกลาง และ ปราศจากอารมณ์...\nเราเรียกภาษาแบบนี้ว่าอะไร?",
        "q2", "alert", 0.5, "Question 2: Evaluating..."
    ))

    # 6. Quiz 2 Answer
    clips.append(make_clip(
        "KNOWLEDGE CHECK: Q2",
        "\nคำตอบ:\n\n[ ภาษาเขียนระดับทางการ ]\n(Formal Language)",
        "a2", "correct", 1.5, "Answer Verified"
    ))

    # 7. Outro / Credits (Safe Version)
    # ไม่ใส่ข้อมูลส่วนตัวลึกๆ ใส่แค่ชื่อผู้จัดทำ
    outro_img = create_slide_img("MISSION COMPLETE", "ขอบคุณสำหรับการรับชม\n\nThanks for Watching", "End of Transmission")
    outro_clip = ImageClip(outro_img).with_duration(8).with_effects([vfx.CrossFadeOut(1.0)])
    clips.append(outro_clip)

    # --- ASSEMBLING ---
    print("Concatenating Scenes...")
    final_video = concatenate_videoclips(clips, method="compose")

    # --- BACKGROUND MUSIC ---
    if os.path.exists("bgm_ambient.mp3"):
        print("Mixing Audio Tracks...")
        bgm_source = AudioFileClip("bgm_ambient.mp3").with_volume_scaled(0.25) # เบาลงนิดนึงเพื่อให้เสียงพูดชัด
        
        # Loop Logic
        loop_count = math.ceil(final_video.duration / bgm_source.duration) + 1
        bgm_full = concatenate_audioclips([bgm_source] * loop_count)
        bgm_final = bgm_full.subclipped(0, final_video.duration)
        
        # Audio Fade In/Out
        bgm_final = bgm_final.with_effects([afx.AudioFadeIn(2), afx.AudioFadeOut(3)])
        
        final_audio = CompositeAudioClip([final_video.audio, bgm_final])
        final_video = final_video.with_audio(final_audio)

    # --- FINAL RENDER ---
    output_file = "YOUTUBE_READY_1080p.mp4"
    print(f"Rendering {output_file}...")
    print("NOTE: This process is CPU intensive. Please keep Termux open.")
    
    final_video.write_videofile(
        output_file, 
        fps=FPS, 
        codec="libx264", 
        audio_codec="aac",
        bitrate="5000k", # High Bitrate for YouTube
        preset="ultrafast", # Balance speed/quality
        threads=4
    )
    
    print("\n==========================================")
    print(f" SUCCESS! Video ready at: {output_file}")
    print(" Upload to YouTube safe & sound. 💀👍")
    print("==========================================")

if __name__ == "__main__":
    main()
