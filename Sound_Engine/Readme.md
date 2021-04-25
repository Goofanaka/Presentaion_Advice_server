<h1>Sound Engine</h1>

## 연결 방식 : Rest API
corsheader와 whitelist만으로 rest처리 하였습니다. formdata로 들어오는 영상 파일을 작업한 후에 json으로 응답합니다.

## DataBase
Mongodb atlas와 연결하여 사용하였습니다.

## Apps
음성 분석 서버 안에 설계된 분석 어플리케이션은 총 두 개입니다.
1. sttmorph : 형태소 분석, fillerwords 탐색, 어미 분석등 기본적인 자연어 분석 어플리케이션입니다.
2. voice : 음성 주파수 분석을 하는 어플리케이션입니다.

### sttmorph
moviepy 라이브러리를 통해 영상 -> 음성 추출
<br>
boto3 라이브러리를 통해 아마존 sdk 사용
<br>
s3 스토리지에 wav 파일 업로드 -> aws transcribe를 통해 stt 작업 수행
<br>
knolpy와 nltk 라이브러리를 통해 자연어처리 작업 수행

### voice
paar-parsel mouth 라이브러리를 통해 시계열 주파수 데이터를 받아옴

