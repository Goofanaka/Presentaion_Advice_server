from django.urls import path
from voice.views import VoiceCheckView

urlpatterns = [
    path('', VoiceCheckView.as_view())
]
