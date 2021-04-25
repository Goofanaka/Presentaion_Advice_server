# 1. Pose_Engine
자세 분석 서버를 실행시키고, 모델로 분석을 진행하는 부분

# 2. Execution Environment
* Openpose의 pre-trained model을 사용<br>
  설치방법 : https://github.com/CMU-Perceptual-Computing-Lab/openpose openpose-master/models/models 파일에 있는 get models.bat 설치
* 기본 OpenCV는 모델을 읽고, 사용할 때 CPU만을 사용해서 처리속도가 느림. GPU를 사용하면 처리속도가 빨라지는데 사용하기 위해선 환경을 설정해줘야함
  - Windows 환경 
    - 컴퓨터의 그래픽카드를 확인하고 그래픽카드에 맞는 nvidia-driver 버전 설치
    - nvidia-driver 버전에 맞는 CUDA, CuDNN 설치
    - Visual Studio, CMake 설치
    - CUDA, CuDNN 버전에 맞는 OpenCV, OpenCV_contrib 설치
    - CMake를 사용해 OpenCV에서 GPU 사용하도록 빌드
    - 참고 : https://www.youtube.com/watch?v=YsmhKar8oOc
  - linux 환경
    - 컴퓨터의 그래픽카드를 확인하고 그래픽카드에 맞는 nvidia-driver 버전 설치
    - nvidia-driver 버전에 맞는 CUDA, CuDNN 설치
    - CMake 설치
    - CUDA, CuDNN 버전에 맞는 OpenCV, OpenCV_contrib 설치
    - CMake를 사용해 OpenCV에서 GPU 사용하도록 빌드

# 3. Features
* pose/pose_engine.py : Openpose의 모델을 이용하여 발표 자세를 분석하는 파일
