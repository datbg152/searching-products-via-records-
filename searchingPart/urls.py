from django.urls import path
from .views import index, transcribe_audio, search_products_view,get_transcription
from searchingPart.record_audio import start_recording_api, stop_recording_api  # ✅ Import APIs

urlpatterns = [
    path("", index, name="index"),
    path('transcribe/',transcribe_audio, name='transcribe'),
    path("search/", search_products_view, name="search_products"),
    path("record/", start_recording_api, name="start_recording"),  # ✅ Start Recording
    path("stop_record/", stop_recording_api, name="stop_recording"),  # ✅ Stop Recording
    path("get_transcription/<str:filename>/", get_transcription, name="get_transcription"),
   
    
]