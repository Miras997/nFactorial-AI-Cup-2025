# core/podcast_generator.py

VOICE_ONE_NAME = "Alex"
VOICE_TWO_NAME = "Sarah"

def generate_podcast_script(processed_content):
    """Creates a two-voice podcast script from processed content."""
    print("Generating podcast script...")
    script_parts = []
    for i, segment in enumerate(processed_content):
        if i % 2 == 0:
            script_parts.append(f"{VOICE_ONE_NAME}: {segment}")
        else:
            script_parts.append(f"{VOICE_TWO_NAME}: {segment}")
    
    # Add a simple intro and outro
    intro = f"{VOICE_ONE_NAME}: Welcome to your personalized study podcast! Today, we'll be diving into your materials."
    outro = f"{VOICE_TWO_NAME}: And that concludes our session for today. We hope this was helpful!"
    
    full_script = [intro] + script_parts + [outro]
    return "\n".join(full_script) 