# NOT WORKING

import openai
from pathlib import Path

# Set your OpenAI API key
openai.api_key = "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"

# Define the text to convert to speech
text = "Today is a wonderful day to build something people love!"

# Define the output file path
speech_file_path = Path(__file__).parent / "speech.mp3"

# Generate and stream TTS in real-time
response = openai.Audio.transcribe(
    model="tts-1",  # Make sure this is the correct model for TTS
    input=text,
    voice="alloy"  # Replace with the appropriate voice model
)

# Save the audio file
with open(speech_file_path, "wb") as f:
    for chunk in response:
        f.write(chunk)
