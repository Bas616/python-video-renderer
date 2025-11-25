import os
import shutil

# Mapping: "ชื่อเดิม": "ชื่อใหม่"
file_mapping = {
    "bgm_seishinsekai (copy).mp3": "bgm_ambient.mp3",
    "se_jyajyan (copy).wav":      "sfx_intro.mp3",
    "blip02.mp3":                 "sfx_type.mp3",
    "button01a.mp3":              "sfx_transition.mp3", 
    "se_buzzer (copy).wav":       "sfx_alert.mp3",
    "correct_answer1.mp3":        "sfx_correct.mp3",
    
    # Voice Over (รองรับทั้งชื่อเดิมและชื่อที่อาจจะเปลี่ยนไปแล้ว)
    "01_intro.mp3.wav":           "01_intro.mp3",
    "01_intro.mp3":               "01_intro.mp3", # กันเหนียว
    
    "02_definition.mp3":          "02_definition.mp3",
    "03_anatomy.mp3":             "03_anatomy.mp3",
    "04_process.mp3":             "04_process.mp3",
    "05_quiz1_q.mp3":             "05_quiz1_q.mp3",
    "05_quiz1_a.mp3":             "05_quiz1_a.mp3",
    "06_quiz2_q.mp3":             "06_quiz2_q.mp3",
    "06_quiz2_a.mp3":             "06_quiz2_a.mp3"
}

def find_and_move_files():
    print("--- STARTING DEEP SEARCH PROTOCOL ---")
    current_dir = os.getcwd()
    found_count = 0
    
    # 1. สร้าง List รายชื่อไฟล์ที่เราต้องการ (เฉพาะชื่อไฟล์เดิม)
    target_filenames = list(file_mapping.keys())
    
    # 2. เดินค้นหาทุกซอกทุกมุม (os.walk)
    for root, dirs, files in os.walk(current_dir):
        for file in files:
            if file in target_filenames:
                # เจอเป้าหมาย!
                old_path = os.path.join(root, file)
                new_filename = file_mapping[file]
                new_path = os.path.join(current_dir, new_filename)
                
                # ถ้าไฟล์ต้นทางกับปลายทางคือไฟล์เดียวกัน (อยู่ใน root แล้ว และชื่อถูกแล้ว)
                if old_path == new_path:
                    print(f"[SKIP] '{file}' is already in place.")
                    continue

                try:
                    # ถ้ามีไฟล์ชื่อใหม่รออยู่แล้ว ให้ลบของเก่าทิ้งก่อน (เพื่อเขียนทับ)
                    if os.path.exists(new_path):
                        os.remove(new_path)
                        
                    # ย้ายและเปลี่ยนชื่อ
                    shutil.move(old_path, new_path)
                    print(f"[MOVED] Found in '{root}' -> Renamed to '{new_filename}'")
                    found_count += 1
                    
                except Exception as e:
                    print(f"[ERROR] Could not move '{file}': {e}")

    print("-" * 40)
    print(f"MISSION REPORT: {found_count} files relocated and renamed.")
    print("Check your folder. Audio assets should be ready. 💀👍")

if __name__ == "__main__":
    find_and_move_files()
