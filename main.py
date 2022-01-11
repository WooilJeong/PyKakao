from PyKakao import KakaoLocal
from pprint import pprint
from config import Config

config=Config()

# 카카오 로컬 API 인증키
service_key = config.OPEN_API['kakao']

# 카카오 로컬 API 세션 정의
KL = KakaoLocal(service_key)

address = "백현동 541"
result = KL.search_address(address)
pprint(result)