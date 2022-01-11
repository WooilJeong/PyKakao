import json
import requests
import logging


## 카카오 로컬 API
class KakaoLocal:
    """
    카카오 로컬 API 핸들러
    """
    def __init__(self, service_key, logger = None):

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
        01 주소 검색
        """
        params = {"query": f"{query}"}

        if analyze_type != None:
            params["analyze_type"] = f"{analyze_type}"

        if page != None:
            params['page'] = f"{page}"

        if size != None:
            params['size'] = f"{size}"

        res = requests.get(self.URL_01, headers=self.headers, params=params)
        document = json.loads(res.text)

        return document


    def geo_coord2regioncode(self, x, y, input_coord=None, output_coord=None):
        """
        02 좌표-행정구역정보 변환
        """
        params = {"x": f"{x}",
                  "y": f"{y}"}
        
        if input_coord != None:
            params['input_coord'] = f"{input_coord}"
        
        if output_coord != None:
            params['output_coord'] = f"{output_coord}"
            
        res = requests.get(self.URL_02, headers=self.headers, params=params)
        document = json.loads(res.text)
        
        return document


    def geo_coord2address(self, x, y, input_coord=None):
        """
        03 좌표-주소 변환
        """
        params = {"x": f"{x}",
                  "y": f"{y}"}
        
        if input_coord != None:
            params['input_coord'] = f"{input_coord}"
            
        res = requests.get(self.URL_03, headers=self.headers, params=params)
        document = json.loads(res.text)
        
        return document


    def geo_transcoord(self, x, y, output_coord, input_coord=None):
        """
        04 좌표계 변환
        """
        params = {"x": f"{x}",
                  "y": f"{y}",
                  "output_coord": f"{output_coord}"}
        
        if input_coord != None:
            params['input_coord'] = f"{input_coord}"
        
        res = requests.get(self.URL_04, headers=self.headers, params=params)
        document = json.loads(res.text)
        
        return document


    def search_keyword(self,query,category_group_code=None,x=None,y=None,radius=None,rect=None,page=None,size=None,sort=None):
        """
        05 키워드 검색
        """
        params = {"query": f"{query}"}
        
        if category_group_code != None:
            params['category_group_code'] = f"{category_group_code}"
        if x != None:
            params['x'] = f"{x}"
        if y != None:
            params['y'] = f"{y}"
        if radius != None:
            params['radius'] = f"{radius}"
        if rect != None:
            params['rect'] = f"{rect}"
        if page != None:
            params['page'] = f"{page}"
        if size != None:
            params['size'] = f"{params}"
        if sort != None:
            params['sort'] = f"{sort}"
        
        res = requests.get(self.URL_05, headers=self.headers, params=params)
        document = json.loads(res.text)
        
        return document


    def search_category(self, category_group_code, x, y, radius=None, rect=None, page=None, size=None, sort=None):
        """
        06 카테고리 검색
        """
        params = {'category_group_code': f"{category_group_code}",
                  'x': f"{x}",
                  'y': f"{y}"}
        
        if radius != None:
            params['radius'] = f"{radius}"
        if rect != None:
            params['rect'] = f"{rect}"
        if page != None:
            params['page'] = f"{page}"
        if size != None:
            params['size'] = f"{size}"
        if sort != None:
            params['sort'] = f"{sort}"
            
        res = requests.get(self.URL_06, headers=self.headers, params=params)
        document = json.loads(res.text)
        
        return document