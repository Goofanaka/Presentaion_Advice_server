from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from sttmorph.models import Stt_Morph
from Presentation.settings import MEDIA_ROOT
from urllib import request as rq
from django.views.decorators.csrf import csrf_exempt
from sttmorph import nlpcheck
import moviepy.editor as mp
import boto3
import time
import json
import re
import math


# Create your views here.

@csrf_exempt
def upload(request):
    if request.method=='POST':
        print(type(request))
        #저장시 특수문자 제거
        pattern = re.compile('[-+=+,#/\?:^$@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》 ]')
        
        #포스트로 온 영상 파일 저장
        file = request.FILES['file']
        file_name = file.name
        file_name = re.sub(pattern, '', file_name)
        file_path = MEDIA_ROOT + file_name
        
        #media 디렉토리에 저장
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        
        #media 디렉토리에서 영상에서 음성 파일 추출
        clip = mp.VideoFileClip(MEDIA_ROOT + file_name)
        clip.audio.write_audiofile(MEDIA_ROOT +'/sample.wav')
        
        #음성 stt 시작
        bucket_name = 'goofanaka-stt-test'
        
        #access key
        aws_access_key_id='YOUR ID'
        aws_secret_access_key='YOUR SECRET KEY'
        s3 = boto3.client('s3', # 사용할 서비스 이름 by.기훈
                  aws_access_key_id=aws_access_key_id, # 액세스키 by.기훈
                  aws_secret_access_key=aws_secret_access_key, # 시크릿 키 by.기훈
                  region_name='ap-northeast-2' # 사용하는 서버 위치 by.기훈
                  )
        
        #s3 버켓에 업로드
        s3.upload_file(file_path, # 버켓에 저장할 파일의 경로 입니다.
               bucket_name, # 저장 할 버켓의 이름입니다.
               file_name) # 버켓에 저장될 파일 이름입니다.
                
        #aws transcrbie stt
        s3_uri = f's3://{bucket_name}/'

        file_format = file_name[file_name.find('.')+1:]

        transcribe = boto3.client('transcribe',
                          aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key,
                          region_name='ap-northeast-2'
                          )
        
        
        #중복시 job_name있을시 job_name에 1을 붙여서 넣어줌
        cnt = 0
        job_name = file_name
        while True:
            try:
                job_uri = f"s3://{bucket_name}/{file_name}"
                transcribe.start_transcription_job(
                    TranscriptionJobName=job_name, # 중복 노노, 이름은 자유롭게 설정 가능
                    Media={'MediaFileUri': job_uri}, # s3 버켓에 올라가 있는 음성 파일 경로(s3-uri)
                    MediaFormat=file_format, # 파일의 포맷(m4a = mp4, mp3, wav, flac...)
                    LanguageCode='ko-KR' # 언어 설정
                )
                
                print('success')
                break
            except:
                cnt += 1
                job_name = str(cnt) + file_name

            
        #STT 실행
        while True:
            status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
            if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
                break
            time.sleep(5)
        
        #STT 결과를 가져옴
        url = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
        raw = rq.urlopen(url).read()

        json_result = json.loads(raw)
        
        
        #전체 발화 텍스트에서 띄어쓰기, 온점, 쉼표 제거
        p = re.compile(r'[ .,]')
        text = json_result['results']['transcripts'][0]['transcript']
        text = re.sub(p, '', text)
        
        #발화 시작 시간
        start = json_result['results']['items'][0]['start_time']
        
        # 발화 종료 시간
        end = json_result['results']['items'][-2]['end_time']

        #전체 발화 시간
        time_duration = float(end) - float(start)

        # 초당 음소 량
        phonem_per_sec = len(text) / time_duration
        
        #발음
        conf = 0
        pronun_cnt = 0
        item = json_result['results']['items']
        for i in range(len(item)):
            if item[i]['type'] == 'punctuation':
                continue
            conf += float(item[i]['alternatives'][0]['confidence'])
            pronun_cnt += 1
        
        json_result['pronunciation'] = float(round(conf / pronun_cnt * 100, 2))
        json_result['time_duration'] = round(time_duration, 2)
        json_result['sylab_per_min'] = int(phonem_per_sec * 60)
        
        #형태소 처리 from 주아
        text = json_result['results']['transcripts'][0]['transcript']
        
        json_result['fillerwords'] = nlpcheck.filler_words_check(text)
        json_result['ttr_check'] = nlpcheck.ttr_check(text)
        json_result['speak_end'] = nlpcheck.word_end_check(text)
        json_result['word_list'] = nlpcheck.get_nouns_list(text)
        
        #불필요한 데이터 처리
        del json_result['results']
        
        #디비에 업로드
        model = Stt_Morph(
            data=json_result
        )
        model.save()
                   
        return JsonResponse({'stt_json' : json_result}, status=200)

    else:
        return HttpResponse('<h1>failed</h1>')
    
def stt(request):
    pass
    