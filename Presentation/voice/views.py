from django.core.files.storage import default_storage
from voice.Voice_Check import Sound_Check_Class
from django.views import View
from django.http import JsonResponse, HttpResponse
from voice.models import *
import moviepy.editor as mp
from Presentation import settings
import os
# Create your views here.

class VoiceCheckView(View):
    # post로 들어온 요청을 받아 voice 엔진을 실행시키고 json을 리턴해주는 함수입니다.
    def post(self,request):
        video_file = request.FILES['file']
        sex = request.POST['gender']
        ## 폼데이터로 비디오영상을 받고 로컬에 저장.
        default_storage.save(video_file.name, video_file)
        
        #파일이름만 빼오기 확장자 빼고 ex) man.mp4 -> man
        file_name =video_file.name.split('.')[0]

        file_path = os.path.join(settings.MEDIA_ROOT, video_file.name)

        clip = mp.VideoFileClip(file_path)

        res = file_name+'.wav'
        # wav파일로 변환
        clip.audio.write_audiofile(res)


        voice_json = Sound_Check_Class.voice_run(res, sex)
        # voice 엔진 실행 후 결과 데이터를 DB에 저장.
        model = voice(data=voice_json)
        model.save()
        return JsonResponse({'voice_json': voice_json}, status=200)