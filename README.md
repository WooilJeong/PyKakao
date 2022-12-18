<div align="center">

<b>카카오 API를 사용하기 위한 오픈소스 로우코드 파이썬 라이브러리</b><br>
<b>🚀`pip install PyKakao --upgrade`</b>

[![PyPI Latest Release](https://img.shields.io/pypi/v/pykakao.svg)](https://pypi.org/project/pykakao/)
[![License](https://img.shields.io/pypi/l/ansicolortags.svg)](https://img.shields.io/pypi/l/ansicolortags.svg)
[![Python](https://img.shields.io/badge/Official-Docs-tomato)](https://wooiljeong.github.io/PyKakao/)
![](https://img.shields.io/badge/API-KAKAO-yellow.svg)  
[![오픈채팅](https://img.shields.io/badge/오픈채팅-Q&A-yellow?logo=KakaoTalk)](https://open.kakao.com/o/gh1N1kJe)

<br>

<div align="left">

## PyKakao

**PyKakao** 라이브러리를 사용하면 [Kakao Developers](https://developers.kakao.com/)에서 제공하는 여러 종류의 카카오 API를 파이썬으로 쉽게 사용할 수 있습니다. 예를 들어, [Daum 검색 API](https://developers.kakao.com/docs/latest/ko/daum-search/dev-guide)를 이용해서 웹에서 정보를 검색할 수 있고, [메시지 API](https://developers.kakao.com/docs/latest/ko/message/rest-api)를 사용해서 카카오톡 메시지를 전송할 수 있습니다. 또한, [로컬 API](https://developers.kakao.com/docs/latest/ko/local/dev-guide)를 통해 주변 정보를 조회할 수 있고, [KoGPT API](https://developers.kakao.com/docs/latest/ko/kogpt/rest-api)를 이용해서 자연어 처리를 할 수 있습니다.


<br>

## 설치 방법

1. 운영체제(OS)에 따라 아래 중 하나를 선택합니다.

- Windows: CMD(명령 프롬프트) 실행
- Mac: Terminal(터미널) 실행

2. 아래 Shell 명령어를 입력 후 실행합니다.

```bash
pip install PyKakao --upgrade
```

<br>

## REST API 키 발급 방법

PyKakao 라이브러리로 카카오 API를 사용하기 위해서는 [Kakao Developers](https://developers.kakao.com/)에 가입해야 합니다. 가입 후 로그인한 상태에서 상단 메뉴의 [내 애플리케이션](https://developers.kakao.com/console/app)을 선택합니다. '애플리케이션 추가하기'를 눌러 팝업창이 뜨면 '앱 이름', '사업자명'을 입력하고, 운영정책에 동의 후 '저장'을 선택합니다. 추가한 애플리케이션을 선택하면 '앱 키' 아래에 '**REST API 키**'가 생성된 것을 확인할 수 있습니다.


<br>

## 사용 방법

### Daum 검색 API

```python
from PyKakao import DaumSearch

# Daum 검색 API 인스턴스 생성
DAUM = DaumSearch(service_key = "REST API 키")

# 웹문서 검색
df = DAUM.search_web("파이썬", dataframe=True)

# 동영상 검색
df = DAUM.search_vclip("파이썬", dataframe=True)

# 이미지 검색
df = DAUM.search_image("파이썬", dataframe=True)

# 블로그 검색
df = DAUM.search_blog("파이썬", dataframe=True)

# 책 검색
df = DAUM.search_book("파이썬", dataframe=True)

# 카페 검색
df = DAUM.search_cafe("파이썬", dataframe=True)
```


### 메시지 API

```python
from PyKakao import Message

# 메시지 API 인스턴스 생성
MSG = Message(service_key = "REST API 키")

# 카카오 인증코드 발급 URL 생성
auth_url = MSG.get_url_for_generatiing_code()
print(auth_url)

# 카카오 인증코드 발급 URL 접속 후 리다이렉트된 URL
url = ""

# 위 URL로 액세스 토큰 추출
access_token = MSG.get_access_token_by_redirected_url(url)

# 액세스 토큰 설정
MSG.set_access_token(access_token)

# 텍스트 메시지 전송
text = "텍스트 영역입니다. 최대 200자 표시 가능합니다."
link = {
            "web_url": "https://developers.kakao.com",
            "mobile_web_url": "https://developers.kakao.com"
        }
button_title = "바로 확인"

MSG.send_text(text=text, link={}, button_title=button_title)
```


### 로컬 API

```python
from PyKakao import Local

# 로컬 API 인스턴스 생성
LOCAL = Local(service_key = "REST API 키")

# 주소 검색하기
df =  LOCAL.search_address("백현동", dataframe=True)

# 좌표로 행정구역정보 받기
df =  LOCAL.geo_coord2regioncode(127.110871319215, 37.3885490672089, dataframe=True)

# 좌표로 주소 변환하기
df =  LOCAL.geo_coord2address(127.110871319215, 37.3885490672089, dataframe=True)

# 좌표계 변환하기
df =  LOCAL.geo_transcoord(127.110871319215, 37.3885490672089, "WCONGNAMUL", dataframe=True)

# 키워드로 장소 검색하기
df =  LOCAL.search_keyword("판교역", dataframe=True)

# 카테고리로 장소 검색하기
df =  LOCAL.search_category("MT1", x=127.110871319215, y=37.3885490672089, radius=500, dataframe=True)
```


### KoGPT API

```python
from PyKako import KoGPT

# KoGPT API 인스턴스 생성
GPT = KoGPT(service_key = "REST API 키")

# 다음 문장 만들기
prompt = "인간처럼 생각하고, 행동하는 '지능'을 통해 인류가 이제까지 풀지 못했던"
max_tokens = 64
result = GPT.generate(prompt, max_tokens, temperature=0.7, top_p=0.8)
```


<br>

## 참고

- **튜토리얼**  
    - [PyKakao - 카카오 API 파이썬 라이브러리](https://wooiljeong.github.io/python/pykakao/)

- **공식문서**
  - [Docs](https://wooiljeong.github.io/PyKakao/)

- **문의**  
  - **이메일**: wooil@kakao.com  
  - **카카오톡 오픈채팅방**: [접속 링크](https://open.kakao.com/o/gh1N1kJe)

<br>

## 기여자

<a href="https://github.com/wooiljeong/pykakao/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=wooiljeong/pykakao" />
</a>

<br>

<div align=center>

[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2FWooilJeong%2FPyKakao&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)

</div>