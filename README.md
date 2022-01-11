# PyKakao

![](https://img.shields.io/badge/python-3.8-blue.svg)
![](https://img.shields.io/badge/requests-2.27.1-red.svg)
[![Linkedin Badge](https://img.shields.io/badge/-WooilJeong-blue?style=plastic&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/wooil/)](https://www.linkedin.com/in/wooil/) 


## 설치

```bash
pip install PyKakao
```

## 예제

```python
from PyKakao import KakaoLocal
from pprint import pprint

# 카카오 로컬 API 인증키
service_key = "카카오 API 인증키"

# 카카오 로컬 API 세션 정의
KL = KakaoLocal(service_key)

# 주소명
address = "백현동 541"
result = KL.search_address(address)
pprint(result)
```

```
{'documents': [{'address': {'address_name': '경기 성남시 분당구 백현동 541',
                            'b_code': '4113511000',
                            'h_code': '4113565700',
                            'main_address_no': '541',
                            'mountain_yn': 'N',
                            'region_1depth_name': '경기',
                            'region_2depth_name': '성남시 분당구',
                            'region_3depth_h_name': '백현동',
                            'region_3depth_name': '백현동',
                            'sub_address_no': '',
                            'x': '127.112037135835',
                            'y': '37.3926536571583'},
                'address_name': '경기 성남시 분당구 백현동 541',
                'address_type': 'REGION_ADDR',
                'road_address': {'address_name': '경기 성남시 분당구 판교역로146번길 20',
                                 'building_name': '현대백화점 판교점',
                                 'main_building_no': '20',
                                 'region_1depth_name': '경기',
                                 'region_2depth_name': '성남시 분당구',
                                 'region_3depth_name': '백현동',
                                 'road_name': '판교역로146번길',
                                 'sub_building_no': '',
                                 'underground_yn': 'N',
                                 'x': '127.112017130086',
                                 'y': '37.39279369494',
                                 'zone_no': '13529'},
                'x': '127.112037135835',
                'y': '37.3926536571583'}],
 'meta': {'is_end': True, 'pageable_count': 1, 'total_count': 1}}
```