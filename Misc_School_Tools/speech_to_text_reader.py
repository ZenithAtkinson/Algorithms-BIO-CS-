import speech_recognition as sr
from pydub import AudioSegment

def transcribe_audio(mp3_path):
    # Convert MP3 to WAV
    audio = AudioSegment.from_mp3(mp3_path)
    wav_path = mp3_path.replace(".mp3", ".wav")
    audio.export(wav_path, format="wav")
    
    # Initialize recognizer
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio_data = recognizer.record(source)
        try:
            # Perform transcription
            transcription = recognizer.recognize_google(audio_data)
            return transcription
        except sr.UnknownValueError:
            return "Could not understand the audio."
        except sr.RequestError as e:
            return f"Error with the transcription service: {e}"

# Path to your MP3 file
mp3_file_path = "path/to/your/audio/file.mp3"
transcript = transcribe_audio(mp3_file_path)
print("Transcription:\n", transcript)
