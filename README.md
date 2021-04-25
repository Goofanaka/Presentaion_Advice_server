# 1. Presentation_Advice
* 프로젝트 명 : 발표의 참견 
* 개요 : 사용자의 발표 영상을 인공지능 시스템이 언어/비언어적 표현을 분석 후 발표 능력 측정 및 피드백을 제공하는 웹 어플리케이션. 자세, 어투, 속도, 발음, 표정 등 다양한 지표를 통해 분석을 진행하여 객관적이고 구체적인 측정 결과를 제공한다. 측정 결과를 기반으로 피드백을 제공하여 사용자의 발표 능력 향상에 기여한다.
* 팀명 : Goofanaka 
* 팀원 : 손기훈 김동건 유주아 김은찬
* 개발 기간 : 2021년 01월 19일 ~ 2021년 4월 28일
___

# 2. Technologies
- 개발언어 : Python
- 모델 구현 : OpenPose, OpenCV, Mediapipe, Tensorflow2.0, Praat-Parselmouth, Amazon Transcribe, Numpy, Pandas
- 데이터베이스 : MongoDB Atlas
- 웹 구현 : Java Script, Django, AWS EC2

___

# 3. Features
- Pose_Engine : 자세 분석 서버를 실행시키고, 모델로 분석을 진행
- Sound_Engine : 음성 분석 서버를 실행시키고, 모델로 분석을 진행
- Face_Engine : 얼굴 분석 서버를 실행시키고, 모델로 분석을 진행
- Web : 웹 대문 서버를 실행시키고, 각 분석 서버에 영상 데이터 전송
