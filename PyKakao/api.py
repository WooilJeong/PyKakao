import json
import requests
import logging


## 카카오 로컬 API
class KakaoLocal:
    """
    카카오 로컬 API 클래스
    """

    def __init__(self, service_key, logger=None):

        if logger is None:
            self.logger = logging.getLogger("root")
        else:
            self.logger = logger

        self.service_key = service_key
        self.headers = {"Authorization": "KakaoAK {}".format(self.service_key)}

        # 서비스 별 URL 설정
        # 01 주소 검색
        self.URL_01 = "https://dapi.kakao.com/v2/local/search/address.json"
        # 02 좌표-행정구역정보 변환
        self.URL_02 = "https://dapi.kakao.com/v2/local/geo/coord2regioncode.json"
        # 03 좌표-주소 변환
        self.URL_03 = "https://dapi.kakao.com/v2/local/geo/coord2address.json"
        # 04 좌표계 변환
        self.URL_04 = "https://dapi.kakao.com/v2/local/geo/transcoord.json"
        # 05 키워드 검색
        self.URL_05 = "https://dapi.kakao.com/v2/local/search/keyword.json"
        # 06 카테고리 검색
        self.URL_06 = "https://dapi.kakao.com/v2/local/search/category.json"

    def search_address(self, query, analyze_type=None, page=None, size=None):
        """
        주소 검색하기

        Args:
            query (str): 검색을 원하는 질의어
        """
        params = {"query": f"{query}"}

        if analyze_type != None:
            params["analyze_type"] = f"{analyze_type}"

        if page != None:
            params["page"] = f"{page}"

        if size != None:
            params["size"] = f"{size}"

        res = requests.get(self.URL_01, headers=self.headers, params=params)
        document = json.loads(res.text)

        return document

    def geo_coord2regioncode(self, x, y, input_coord=None, output_coord=None):
        """
        좌표로 행정구역정보 받기

        Args:
            x (str): X 좌표값, 경위도인 경우 경도(longitude)
            y (str): Y 좌표값, 경위도인 경우 위도(latitude)
            input_coord (str): x, y 로 입력되는 값에 대한 좌표계. 지원 좌표계: WGS84, WCONGNAMUL, CONGNAMUL, WTM, TM (기본값: WGS84)
            output_coord (str): 결과에 출력될 좌표계. 지원 좌표계: WGS84, WCONGNAMUL, CONGNAMUL, WTM, TM (기본값: WGS84)
        """
        params = {"x": f"{x}", "y": f"{y}"}

        if input_coord != None:
            params["input_coord"] = f"{input_coord}"

        if output_coord != None:
            params["output_coord"] = f"{output_coord}"

        res = requests.get(self.URL_02, headers=self.headers, params=params)
        document = json.loads(res.text)

        return document

    def geo_coord2address(self, x, y, input_coord=None):
        """
        좌표로 주소 변환하기

        Args:
            x (str): X 좌표값, 경위도인 경우 경도(longitude)
            y (str): Y 좌표값, 경위도인 경우 위도(latitude)
            input_coords (str): x, y 로 입력되는 값에 대한 좌표계. 지원 좌표계: WGS84, WCONGNAMUL, CONGNAMUL, WTM, TM (기본값: WGS84)
        """
        params = {"x": f"{x}", "y": f"{y}"}

        if input_coord != None:
            params["input_coord"] = f"{input_coord}"

        res = requests.get(self.URL_03, headers=self.headers, params=params)
        document = json.loads(res.text)

        return document

    def geo_transcoord(self, x, y, output_coord, input_coord=None):
        """
        좌표계 변환하기

        Args:
            x (str): X 좌표값, 경위도인 경우 longitude(경도)
            y (str): Y 좌표값, 경위도인 경우 latitude(위도)
            output_coord (str): x, y 값의 좌표계. 지원 좌표계: WGS84, WCONGNAMUL, CONGNAMUL, WTM, TM, KTM, UTM, BESSEL, WKTM, WUTM (기본값: WGS84)
            input_coord (str): 변환할 좌표계. 지원 좌표계:WGS84, WCONGNAMUL, CONGNAMUL, WTM, TM, KTM, UTM, BESSEL, WKTM, WUTM (기본값: WGS84)
        """
        params = {"x": f"{x}", "y": f"{y}", "output_coord": f"{output_coord}"}

        if input_coord != None:
            params["input_coord"] = f"{input_coord}"

        res = requests.get(self.URL_04, headers=self.headers, params=params)
        document = json.loads(res.text)

        return document

    def search_keyword(
        self,
        query,
        category_group_code=None,
        x=None,
        y=None,
        radius=None,
        rect=None,
        page=None,
        size=None,
        sort=None,
    ):
        """
        키워드로 장소 검색하기

        Args:
            query (str): 검색을 원하는 질의어
            category_group_code (str): [카테고리 그룹 코드](https://developers.kakao.com/docs/latest/ko/local/dev-guide#search-by-keyword-request-category-group-code) 카테고리로 결과 필터링을 원하는 경우 사용
            x (str): 중심 좌표의 X 혹은 경도(longitude) 값. 특정 지역을 중심으로 검색할 경우 radius와 함께 사용 가능
            y (str): 중심 좌표의 Y 혹은 위도(latitude) 값. 특정 지역을 중심으로 검색할 경우 radius와 함께 사용 가능
            radius (str): 중심 좌표부터의 반경거리. 특정 지역을 중심으로 검색하려고 할 경우 중심좌표로 쓰일 x,y와 함께 사용. (단위: 미터(m), 최소: 0, 최대: 20000)
            rect (str): 사각형의 지정 범위 내 제한 검색을 위한 좌표. 지도 화면 내 검색 등 제한 검색에서 사용 가능. 좌측 X 좌표, 좌측 Y 좌표, 우측 X 좌표, 우측 Y 좌표 형식
            page (str): 결과 페이지 번호. (최소: 1, 최대: 45, 기본값: 1)
            size (str): 한 페이지에 보여질 문서의 개수. (최소: 1, 최대: 45, 기본값: 15)
            sort (str): 결과 정렬 순서. distance 정렬을 원할 때는 기준 좌표로 쓰일 x, y와 함께 사용 distance 또는 accuracy(기본값: accuracy)
        """
        params = {"query": f"{query}"}

        if category_group_code != None:
            params["category_group_code"] = f"{category_group_code}"
        if x != None:
            params["x"] = f"{x}"
        if y != None:
            params["y"] = f"{y}"
        if radius != None:
            params["radius"] = f"{radius}"
        if rect != None:
            params["rect"] = f"{rect}"
        if page != None:
            params["page"] = f"{page}"
        if size != None:
            params["size"] = f"{params}"
        if sort != None:
            params["sort"] = f"{sort}"

        res = requests.get(self.URL_05, headers=self.headers, params=params)
        document = json.loads(res.text)

        return document

    def search_category(
        self,
        category_group_code,
        x,
        y,
        radius=None,
        rect=None,
        page=None,
        size=None,
        sort=None,
    ):
        """
        카테고리로 장소 검색하기

        Args:
            category_group_code (str): [카테고리 코드](https://developers.kakao.com/docs/latest/ko/local/dev-guide#search-by-category-request-category-group-code)
            x (str): 중심 좌표의 X값 혹은 longitude. 특정 지역을 중심으로 검색하려고 할 경우 radius와 함께 사용 가능.
            y (str): 중심 좌표의 Y값 혹은 latitude. 특정 지역을 중심으로 검색하려고 할 경우 radius와 함께 사용 가능.
            radius (str): 중심 좌표부터의 반경거리. 특정 지역을 중심으로 검색하려고 할 경우 중심좌표로 쓰일 x,y와 함께 사용. 단위 meter, 0~20000 사이의 값
            rect (str): 사각형 범위내에서 제한 검색을 위한 좌표. 지도 화면 내 검색시 등 제한 검색에서 사용 가능. 좌측 X 좌표, 좌측 Y 좌표, 우측 X 좌표, 우측 Y 좌표 형식. x, y, radius 또는 rect 필수
            page (str): 결과 페이지 번호. 1~45 사이의 값 (기본값: 1)
            size (str): 한 페이지에 보여질 문서의 개수. 1~15 사이의 값 (기본값: 15)
            sort (str): 결과 정렬 순서, distance 정렬을 원할 때는 기준좌표로 쓰일 x, y 파라미터 필요. distance 또는 accuracy (기본값: accuracy)
        """
        params = {
            "category_group_code": f"{category_group_code}",
            "x": f"{x}",
            "y": f"{y}",
        }

        if radius != None:
            params["radius"] = f"{radius}"
        if rect != None:
            params["rect"] = f"{rect}"
        if page != None:
            params["page"] = f"{page}"
        if size != None:
            params["size"] = f"{size}"
        if sort != None:
            params["sort"] = f"{sort}"

        res = requests.get(self.URL_06, headers=self.headers, params=params)
        document = json.loads(res.text)

        return document
