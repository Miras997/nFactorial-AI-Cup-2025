# core/tts_handler.py
from gtts import gTTS
import os

# In a more advanced setup, we might use different voices or TTS engines here.
# For gTTS, distinguishing voices directly is hard. We rely on the script to denote speakers.

def text_to_speech(text, filename, lang='en', voice_id="voice1"):
    """Converts a single text segment to speech and saves it.
    The voice_id is a placeholder for future enhancements where different TTS engines
    or configurations could be used for distinct voices.
    """
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(filename)
        print(f"Audio segment saved: {filename} for {voice_id}")
        return True
    except Exception as e:
        print(f"Error in gTTS for {voice_id} with text '{text[:30]}...': {e}")
        return False

def generate_podcast_audio(script_lines, output_filename_base, output_dir="output_podcasts"):
    """Generates audio for each line of the script, naming them for later processing.
    Currently, this will produce separate files for each line by a single voice model.
    A more sophisticated approach would involve using pydub to stitch these, potentially
    with different voice characteristics if the TTS supported it.
    For now, we'll focus on generating based on the script line by line and saving them.
    A single combined audio file is a future step with pydub.
    """
    print("Generating podcast audio segments...")
    # For simplicity in this version, we'll just generate one audio file for the whole script.
    # True multi-voice with gTTS and combining with pydub adds complexity we can iterate on.
    
    full_script_text = "\n".join([line.split(": ", 1)[1] if ": " in line else line for line in script_lines])
    
    output_path = os.path.join(output_dir, f"{output_filename_base}.mp3")

    if text_to_speech(full_script_text, output_path, voice_id="combined"):
        print(f"Full podcast audio saved: {output_path}")
        return output_path
    else:
        print(f"Failed to generate full podcast audio.")
        return None 