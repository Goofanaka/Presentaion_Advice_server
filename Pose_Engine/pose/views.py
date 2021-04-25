from django.views import View
from django.http import JsonResponse
from pose.pose_engine import Pose_Check
from django.core.files.storage import default_storage
from pose_check.settings import MEDIA_ROOT
from pose.models import Pose

# post로 들어온 요청을 받아 pose엔진을 실행시키고 json을 리턴해주는 함수입니다.
class PoseCheckView(View):
    def post(self, request):
        # 폼데이터로 비디오영상을 받고 로컬에 저장.
        video_file = request.FILES['file']
        default_storage.save(MEDIA_ROOT+video_file.name, video_file)

        # 저장한 비디오영상으로 pose엔진 실행.
        pose_json = Pose_Check.pose_run(self, MEDIA_ROOT, video_file.name)
        
        # pose엔진 실행 후 결과 데이터를 DB에 저장.
        model = Pose(data=pose_json)
        model.save()

        # pose엔진 실행 후 결과 데이터를 json형식으로 응답해줌.
        return JsonResponse({'pose_json' : pose_json}, status=200)