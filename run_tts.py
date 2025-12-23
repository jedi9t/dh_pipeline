# run_tts.py
import asyncio
import edge_tts
import os
from deep_translator import GoogleTranslator


TEXT_FILE = "inputs/text.txt"
OUTPUT_DIR = "outputs/tts"


TTS_CONFIGS = [
    {
        "target_lang": "source", # source mark, don't translate
        "voice": "zh-CN-YunyangNeural", 
        "desc": "Original sound"
    },
    {
        "target_lang": "en", 
        "voice": "en-US-EricNeural", 
        "desc": "English"
    },
    {
        "target_lang": "es", 
        "voice": "es-ES-AlvaroNeural", 
        "desc": "Spanish"
    },
    {
        "target_lang": "ja", 
        "voice": "ja-JP-KeitaNeural", 
        "desc": "Japanese"
    }
]

# ------------
async def generate_audio(text, voice, output_path, desc):
    """A function to handle audio generation separately"""
    print(f"[{desc}] Generating speech ({voice})...")
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)
    print(f"[{desc}] Speech saved to: {output_path}")

async def main():
    # 1. Check input file
    if not os.path.exists(TEXT_FILE):
        print(f"Error: Text file not found {TEXT_FILE}")
        return

    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 2. Reading source text
    with open(TEXT_FILE, "r", encoding="utf-8") as f:
        source_text = f.read().strip()
    
    if not source_text:
        print("Error: Input text is empety")
        return

    print(f"source text readed, length: {len(source_text)} characters")
    print("-" * 30)

    start_total = asyncio.get_event_loop().time()

    # 3. Iteratly translate and generate audio 
    tasks = [] # Concurently handling（Option）
    
    for config in TTS_CONFIGS:
        current_text = source_text
        lang_code = config["target_lang"]
        voice = config["voice"]
        desc = config["desc"]
        
        # Construct output file path
        output_file = os.path.join(OUTPUT_DIR, f"generated_audio_{voice}.mp3")

        # Translate logic
        if lang_code != "source":
            print(f"[{desc}] Translating (-> {lang_code})...")
            try:
                # take Google Translator translating
                translator = GoogleTranslator(source='zh-CN', target=lang_code)
                current_text = translator.translate(source_text)
                print(f"[{desc}] Translation done: {current_text[:20]}...") # Print first 20 character to verify
            except Exception as e:
                print(f"[{desc}] Translation failed: {e}")
                continue 
        
        # Generate audio        
        await generate_audio(current_text, voice, output_file, desc)

    print("-" * 30)
    print(f"All tasks done, consumed time: {asyncio.get_event_loop().time() - start_total:.2f} seconds")

# ------------
if __name__ == "__main__":
    asyncio.run(main())
