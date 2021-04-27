from nltk.tokenize import word_tokenize
from collections import Counter
from konlpy.tag import Kkma, Okt
from konlpy.utils import pprint

def filler_words_check(txt):
    # filler words 리스트
    filler_words = ['설마', '그렇군요', '그렇구나', '그럼', '아야', '마구', '그러니까', '말하자면', '그다지', '어머나', '맞아요', '저', '있잖아', '아', '그래', '뭐랄까', '그', '뭐라고', '글쎄', '솔직히', '뭐지', '뭐더라', '그래요', '아무튼', '에이', '막', '아이고', '예', '어머', '세상에', '자', '뭐', '우와', '그게', '글쎄요', '정말', '음', '맞아', '어쨌든', '좀', '야', '진짜', '별로', '네', '참', '에휴', '쉿', '어', '저기요', '그냥']

    # 토큰화
    word_tokens = word_tokenize(txt)

    # filler words 체크
    result = []
    result=[word for word in word_tokens if word in filler_words]
    count = Counter(result).most_common()
    
    result_words = []
    for i in range(len(count)):
        temp = {'text' : count[i][0], 'weight' : count[i][1]}
        result_words.append(temp)
        

    # 출력
    # print(word_tokens)
    #print('사용한 fillerwords : {}'.format(result))
    #print('총 사용 횟수 : {}'.format(len(result)))
    #print('filler words별 사용 횟수 : {}'.format(count))
    
    return result_words


def ttr_check(txt):
    # kkma 객체 생성
    kkma = Kkma()
    # 형태소 및 태그 추출
    pos = kkma.pos(txt)
    # 빈도 카운트 및 저장(dict)
    count = Counter(pos)
    # pprint(count)

    # token
    ttr_token = sum(count.values())
    # type
    ttr_type = len(count.keys())
    # TTR
    ttr = (ttr_type / ttr_token) *100

    # 출력
    # print(ttr_token, ttr_type)
    # print('TTR은 : {} 입니다.'.format(ttr))

    return round(ttr, 2)

def word_end_check(txt):
    
    kkma = Kkma()
    # 형태소 및 태그 추출
    pos = kkma.pos(txt)
    # 빈도 카운트 및 저장(dict)
    count = Counter(pos)

    word_a = 0
    word_b = 0
    for i in count.keys() :
        # 의문, 청유형 횟수 카운트
        if i[1] in ('EFQ','EFA') :
            word_a += count[i]
        # 평서, 존칭형 횟수 카운트
        elif i[1] in ('EFN','EFR') :
            word_b += count[i]

    # print(word_a)
    # print(word_b)
    # 참여유도형 화법 비율
    rate1 = word_a / (word_a+word_b) * 100
    # 공식적인 화법 비율
    rate2 = word_b / (word_a+word_b) * 100

    return {'formal_speak' : round(rate2, 2), 'question_speak' : round(rate1, 2)}

def get_nouns_list(txt):
    
    okt = Okt()
    
    nouns = okt.nouns(txt)
    
    nouns = Counter(nouns).most_common()
    print(nouns)
    word_list = []
    
    for i in range(len(nouns)):
        temp = {'text' : nouns[i][0], 'weight' : nouns[i][1]}
        word_list.append(temp)
    print(word_list)    
    return word_list
