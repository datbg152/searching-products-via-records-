import os
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
from searchingPart.search_logic import search_products
import whisper
from searchingPart.transcribe_audio import transcribe_file
from searchingPart.models import Transcription
# Initialize Whisper AI model
model = whisper.load_model("base")  # "tiny", "small", "base", "medium", "large"


@csrf_exempt
def stop_record(request):
    if request.method == "POST":
        audio_file = request.POST.get("audio_file")

        if not audio_file:
            return JsonResponse({"error": "Missing audio_file"}, status=400)

        audio_path = os.path.join("recordings", audio_file)

        if not os.path.exists(audio_path):
            return JsonResponse({"error": "Audio file does not exist"}, status=400)

        # ✅ Automatically trigger transcription here
        transcribed_text = transcribe_file(audio_path)

        return JsonResponse({
            "audio_file": audio_file,
            "transcription": transcribed_text
        })

    return JsonResponse({"error": "Invalid request"}, status=405)
# 📄 1️⃣ Render the index.html page
def index(request):
    return render(request, "searchingPart/index.html")

# 🎤 2️⃣ Handle audio file upload & transcribe it
def transcribe_audio(request):
    audio_file = request.GET.get("audio")

    if not audio_file:
        return JsonResponse({"error": "Audio filename missing"}, status=400)

    audio_path = os.path.join("recordings", audio_file)

    if not os.path.exists(audio_path):
        return JsonResponse({"error": "Audio file not found"}, status=404)

    transcription = transcribe_file(audio_path)

    return JsonResponse({"transcription": transcription})

# 🔍 3️⃣ Handle search request from transcribed text
def search_products_view(request):
    query = request.GET.get("query", "")
    if query:
        results = search_products(query)
        return JsonResponse({"products": [hit["_source"] for hit in results]})
    return JsonResponse({"products": []})


def get_transcription(request, filename):
    """Fetch transcription by filename from PostgreSQL."""
    try:
        transcription = Transcription.objects.get(filename=filename)
        return JsonResponse({"filename": filename, "text": transcription.text})
    except Transcription.DoesNotExist:
        return JsonResponse({"error": "Transcription not found"}, status=404)