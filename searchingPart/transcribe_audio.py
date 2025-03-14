import whisper
import os
import json
import django
import sys

# ✅ Ensure Django setup
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'searchProject.settings')
django.setup()

from searchingPart.models import Transcription

model = whisper.load_model("small")

def transcribe_file(filepath):
    filename = os.path.basename(filepath)

    if Transcription.objects.filter(filename=filename).exists():
        transcription = Transcription.objects.get(filename=filename)
        return transcription.text

    result = model.transcribe(filepath, language="en", temperature=0)
    transcribed_text = result["text"]

    json_data = {
        "filename": filename,
        "text": transcribed_text,
        "language": result.get("language", "unknown")
    }

    json_path = filepath.replace(".wav", ".json")
    with open(json_path, "w", encoding="utf-8") as json_file:
        json.dump(json_data, json_file, indent=4)

    Transcription.objects.create(filename=filename, text=transcribed_text)

    return transcribed_text

# Optional: Transcribe all files when script is run directly
if __name__ == "__main__":
    recordings_folder = "recordings"
    files = sorted([f for f in os.listdir(recordings_folder) if f.endswith(".wav")])

    for file in files:
        audio_path = os.path.join(recordings_folder, file)
        transcribe_file(audio_path)
        print(f"✅ Transcribed and stored: {file}")

    print("\n🎉 All transcriptions complete!")