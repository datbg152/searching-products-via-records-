import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import os
import time
from django.http import JsonResponse

# Create recordings folder if not exists
recordings_folder = "recordings"
os.makedirs(recordings_folder, exist_ok=True)

samplerate = 44100
channels = 1
audio_data = []
recording = False
stream = None  # Store the recording stream globally

def start_recording():
    """Start recording audio."""
    global recording, audio_data, stream
    recording = True
    audio_data = []

    def callback(indata, frames, time, status):
        if status:
            print(status)
        if recording:
            audio_data.append(indata.copy())

    stream = sd.InputStream(callback=callback, samplerate=samplerate, channels=channels)
    stream.start()

def stop_recording():
    """Stop recording and save audio."""
    global recording, stream
    if not recording:
        return None

    recording = False
    if stream:
        stream.stop()
        stream.close()

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(recordings_folder, f"{timestamp}.wav")

    audio_array = np.concatenate(audio_data, axis=0)
    wav.write(filename, samplerate, audio_array)

    print(f"✅ Audio saved as: {filename}")
    return filename

# 🎤 **API to start recording**
def start_recording_api(request):
    start_recording()
    return JsonResponse({"status": "recording started"})

# 🛑 **API to stop recording**
def stop_recording_api(request):
    filename = stop_recording()
    if filename:
        return JsonResponse({"status": "recording stopped", "audio_file": filename})
    return JsonResponse({"status": "no recording found"}, status=400)