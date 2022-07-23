# PyKakao

[![PyPI Latest Release](https://img.shields.io/pypi/v/pykakao.svg)](https://pypi.org/project/pykakao/)
![](https://img.shields.io/badge/python-3.8-blue.svg)
![](https://img.shields.io/badge/requests-2.27.1-red.svg)
![](https://img.shields.io/badge/api-kakao-yellow.svg)

## 기여자

<div align="center">
    <table>
    <tr>
        <td align="center">
            <a href="https://github.com/wooiljeong">
            <img src="https://avatars.githubusercontent.com/u/38076110?v=4" width="100px;" alt=""/><br />
            <sub><b>정우일</b></sub></a><br />
        </td>
    </tr>
    </table>
</div>

## 소개

PyKakao는 [kakao developers](https://developers.kakao.com/)에서 제공하는 [로컬(Local) API](https://developers.kakao.com/docs/latest/ko/local/common)를 이용할 수 있는 Python Client 입니다. PyKakao를 정상적으로 이용하기 위해서는 kakao developers 애플리케이션 추가를 통해 발급되는 REST API 키가 필요합니다.

## 설치

```bash
pip install PyKakao
```

## 예제

### 카카오 로컬 API 기능 불러오기

```python
from PyKakao import KakaoLocal

# kakao developers에서 발급받은 REST API 키	
service_key = "REST API 키"

# kakao local API 세션 정의
KL = KakaoLocal(service_key)
```

### 1. 주소 검색하기

```python
# 1. 주소 검색하기
address = "백현동 541"
result = KL.search_address(address)
result
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

### 2. 좌표로 행정구역정보 받기

```python
# 2. 좌표로 행정구역정보 받기
x, y = 127.11198669812507, 37.392627919703536
result = KL.geo_coord2regioncode(x, y)
result
```

```
{'meta': {'total_count': 2},
 'documents': [{'region_type': 'B',
   'code': '4113511000',
   'address_name': '경기도 성남시 분당구 백현동',
   'region_1depth_name': '경기도',
   'region_2depth_name': '성남시 분당구',
   'region_3depth_name': '백현동',
   'region_4depth_name': '',
   'x': 127.11087131921613,
   'y': 37.388549067217625},
  {'region_type': 'H',
   'code': '4113565700',
   'address_name': '경기도 성남시 분당구 백현동',
   'region_1depth_name': '경기도',
   'region_2depth_name': '성남시 분당구',
   'region_3depth_name': '백현동',
   'region_4depth_name': '',
   'x': 127.11087131921613,
   'y': 37.388549067217625}]}
```

### 3. 좌표로 주소 변환하기

```python
# 3. 좌표로 주소 변환하기
x, y = 127.11198669812507, 37.392627919703536
result = KL.geo_coord2address(x, y)
result
```

```
{'meta': {'total_count': 1},
 'documents': [{'road_address': {'address_name': '경기도 성남시 분당구 판교역로146번길 20',
    'region_1depth_name': '경기',
    'region_2depth_name': '성남시 분당구',
    'region_3depth_name': '',
    'road_name': '판교역로146번길',
    'underground_yn': 'N',
    'main_building_no': '20',
    'sub_building_no': '',
    'building_name': '현대백화점 판교점',
    'zone_no': '13529'},
   'address': {'address_name': '경기 성남시 분당구 백현동 541',
    'region_1depth_name': '경기',
    'region_2depth_name': '성남시 분당구',
    'region_3depth_name': '백현동',
    'mountain_yn': 'N',
    'main_address_no': '541',
    'sub_address_no': '',
    'zip_code': ''}}]}
```

### 4. 좌표계 변환하기

```python
# 4. 좌표계 변환하기
x, y = 127.11198669812507, 37.392627919703536
output_coord = "WTM"
input_coord = "WGS84"
result = KL.geo_transcoord(x, y, output_coord, input_coord)
result
```

```
{'meta': {'total_count': 1},
 'documents': [{'x': 209916.63703445005, 'y': 432593.2082232768}]}
```

### 5. 키워드로 장소 검색하기

```python
# 5. 키워드로 장소 검색하기
query = "스타벅스"
category_group_code = "CE7"                     # 카페
x, y = 127.11198669812507, 37.392627919703536   # 중심 좌표
radius = 500                                    # 반경거리(m)

result = KL.search_keyword(query, category_group_code, x, y, radius)
result
```

```
{'documents': [{'address_name': '경기 성남시 분당구 백현동 537',
   'category_group_code': 'CE7',
   'category_group_name': '카페',
   'category_name': '음식점 > 카페 > 커피전문점 > 스타벅스',
   'distance': '231',
   'id': '382618195',
   'phone': '1522-3232',
   'place_name': '스타벅스 판교알파돔타워',
   'place_url': 'http://place.map.kakao.com/382618195',
   'road_address_name': '경기 성남시 분당구 판교역로 152',
   'x': '127.110364770136',
   'y': '37.3942620223016'},
  {'address_name': '경기 성남시 분당구 백현동 531',
   'category_group_code': 'CE7',
   'category_group_name': '카페',
   'category_name': '음식점 > 카페 > 커피전문점 > 스타벅스',
   'distance': '309',
   'id': '27528340',
   'phone': '1522-3232',
   'place_name': '스타벅스 판교알파돔시티점',
   'place_url': 'http://place.map.kakao.com/27528340',
   'road_address_name': '경기 성남시 분당구 대왕판교로606번길 10',
   'x': '127.109353202048',
   'y': '37.3944611869007'}],
 'meta': {'is_end': True,
  'pageable_count': 2,
  'same_name': {'keyword': '스타벅스', 'region': [], 'selected_region': ''},
  'total_count': 2}}
```

### 6. 카테고리로 장소 검색하기

```python
# 6. 카테고리로 장소 검색하기
category_group_code = "CE7"                     # 카페
x, y = 127.11198669812507, 37.392627919703536   # 중심 좌표
radius = 50                                     # 반경거리(m)

result = KL.search_category(category_group_code, x, y, radius)
result
```

```
{'documents': [{'address_name': '경기 성남시 분당구 백현동 541',
   'category_group_code': 'CE7',
   'category_group_name': '카페',
   'category_name': '음식점 > 카페',
   'distance': '4',
   'id': '1513310698',
   'phone': '031-5170-1354',
   'place_name': '메종키츠네카페',
   'place_url': 'http://place.map.kakao.com/1513310698',
   'road_address_name': '경기 성남시 분당구 판교역로146번길 20',
   'x': '127.11195356152',
   'y': '37.3926486004944'},
  {'address_name': '경기 성남시 분당구 백현동 541',
   'category_group_code': 'CE7',
   'category_group_name': '카페',
   'category_name': '음식점 > 카페 > 커피전문점',
   'distance': '20',
   'id': '768523904',
   'phone': '031-5170-3259',
   'place_name': '카멜커피',
   'place_url': 'http://place.map.kakao.com/768523904',
   'road_address_name': '경기 성남시 분당구 판교역로146번길 20',
   'x': '127.11208816176',
   'y': '37.3927935375378'},
  {'address_name': '경기 성남시 분당구 백현동 541',
   'x': '127.112029412303',
   'y': '37.3927755727699'}],
 'meta': {'is_end': False,
  'pageable_count': 32,
  'same_name': None,
  'total_count': 32}}
```

<br>

<div align=center>

[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2FWooilJeong%2FPyKakao&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)

</div>