from django.core.files.storage import default_storage
from face_test.Face_Check import Eye_check
from django.views import View
from django.http import JsonResponse
from face_test.models import *
# Create your views here.


class FaceCheckView(View):

    # post로 들어온 요청을 받고 face엔진을 실행시키고 json을 리턴해주는 함수입니다. by. 은찬
    def post(self, request):
        # 폼데이터로 비디오영상을 받고 로컬에 저장.
        video_file = request.FILES['file']
        default_storage.save(video_file.name, video_file)
        # 저장한 비디오영상으로 face엔진 실행.
        face_json= Eye_check.face_run(self, video_file.name)

        # MongoDB에 저장
        model = Face(data=face_json)
        model.save()
        return JsonResponse({'face_json': face_json}, status=200)

 
