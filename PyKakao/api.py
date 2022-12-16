import json
import requests
import pandas as pd


class Message:
    """
    카카오 메시지 API 클래스

    Parameters
    ----------
    service_key : str
        카카오 개발자 센터에서 발급받은 애플리케이션의 REST API 키
    """

    def __init__(self, service_key=None, redirect_uri="https://localhost:5000", scope="talk_message"):
        self.service_key = service_key
        self.redirect_uri = redirect_uri
        self.scope = scope
        self.url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

    def get_url_for_generatiing_code(self):
        """
        카카오 인증코드 발급 URL 생성

        Returns
        -------
        str
            카카오 인증코드 발급 URL
        """
        url = f"https://kauth.kakao.com/oauth/authorize?client_id={self.service_key}&redirect_uri={self.redirect_uri}&response_type=code&scope={self.scope}"
        res = requests.get(url).url
        return res

    def get_code_by_redirected_url(self, url):
        """
        카카오 인증코드 추출

        Parameters
        ----------
        url : str
            카카오 인증코드 발급 URL 접속 후 리다이렉트된 URL

        Returns
        -------
        str
            카카오 인증코드
        """
        return url.split("code=")[1]

    def get_access_token_by_code(self, code):
        """
        카카오 인증코드로 액세스 토큰 발급

        Parameters
        ----------
        code : str
            카카오 인증코드

        Returns
        -------
        str
            액세스 토큰
        """
        url = "https://kauth.kakao.com/oauth/token"
        data = {
            "grant_type": "authorization_code",
            "client_id": self.service_key,
            "redirect_uri": self.redirect_uri,
            "code": code,
        }
        r = requests.post(url, data=data)
        return r.json()['access_token']

    def get_access_token_by_redirected_url(self, url):
        """
        카카오 인증코드 발급 URL 접속 후 리다이렉트된 URL로 액세스 토큰 발급

        Parameters
        ----------
        url : str
            카카오 인증코드 발급 URL 접속 후 리다이렉트된 URL

        Returns
        -------
        str
            액세스 토큰
        """
        code = self.get_code_by_redirected_url(url)
        api_url = "https://kauth.kakao.com/oauth/token"
        data = {
            "grant_type": "authorization_code",
            "client_id": self.service_key,
            "redirect_uri": self.redirect_uri,
            "code": code,
        }
        r = requests.post(api_url, data=data)
        return r.json()['access_token']

    def set_access_token(self, access_token):
        """
        액세스 토큰 설정

        Parameters
        ----------
        access_token : str
            액세스 토큰
        """
        self.headers = {"Authorization": f"Bearer {access_token}"}
        print("액세스 토큰 설정 완료")

    def send_text(self, text, link, **kwargs):
        """
        텍스트 메시지 전송

        Parameters
        ----------
        text : str
            전송할 메시지 (최대 200자)
        """
        params = {
            "object_type": "text",
            "text": text,
            "link": link,
        }
        params.update(kwargs)
        data = {"template_object": json.dumps(params)}
        try:
            r = requests.post(self.url, headers=self.headers, data=data)
            r.raise_for_status()
        except Exception as e:
            print(f"메시지 전송 실패")
            print(e)
            return
        if r.json()['result_code'] == 0:
            print("메시지 전송 성공")
        else:
            print(f"메시지 전송 실패")
            print(r.json())

    def send_feed(self, content, **kwargs):
        """
        피드 메시지 전송

        Parameters
        ----------
        content : dict
            피드 내용
        """
        params = {
            "object_type": "feed",
            "content": content,
        }
        params.update(kwargs)
        data = {"template_object": json.dumps(params)}
        try:
            r = requests.post(self.url, headers=self.headers, data=data)
            r.raise_for_status()
        except Exception as e:
            print(f"메시지 전송 실패")
            print(e)
            return
        if r.json()['result_code'] == 0:
            print("메시지 전송 성공")
        else:
            print(f"메시지 전송 실패")
            print(r.json())

    def send_list(self, header_title, header_link, contents, **kwargs):
        """
        리스트 메시지 전송

        Parameters
        ----------
        header_title : str
            리스트 제목
        header_link : dict
            리스트 링크
        contents : list
            리스트 내용
        """
        params = {
            "object_type": "list",
            "header_title": header_title,
            "header_link": header_link,
            "contents": contents,
        }
        params.update(kwargs)
        data = {"template_object": json.dumps(params)}
        try:
            r = requests.post(self.url, headers=self.headers, data=data)
            r.raise_for_status()
        except Exception as e:
            print(f"메시지 전송 실패")
            print(e)
            return
        if r.json()['result_code'] == 0:
            print("메시지 전송 성공")
        else:
            print(f"메시지 전송 실패")
            print(r.json())

    def send_location(self, address, address_title, content, **kwargs):
        """
        위치 메시지 전송

        Parameters
        ----------
        address : str
            주소
        address_title : str
            주소 제목
        content : dict
            위치 정보
        """
        params = {
            "object_type": "location",
            "address": address,
            "address_title": address_title,
            "content": content,
        }
        params.update(kwargs)
        data = {"template_object": json.dumps(params)}
        try:
            r = requests.post(self.url, headers=self.headers, data=data)
            r.raise_for_status()
        except Exception as e:
            print(f"메시지 전송 실패")
            print(e)
            return
        if r.json()['result_code'] == 0:
            print("메시지 전송 성공")
        else:
            print(f"메시지 전송 실패")
            print(r.json())

    def send_commerce(self, content, commerce, **kwargs):
        """
        커머스 메시지 전송

        Parameters
        ----------
        content : dict
            커머스 정보
        commerce : dict
            상품 정보
        """
        params = {
            "object_type": "commerce",
            "content": content,
            "commerce": commerce,
        }
        params.update(kwargs)
        data = {"template_object": json.dumps(params)}
        try:
            r = requests.post(self.url, headers=self.headers, data=data)
            r.raise_for_status()
        except Exception as e:
            print(f"메시지 전송 실패")
            print(e)
            return
        if r.json()['result_code'] == 0:
            print("메시지 전송 성공")
        else:
            print(f"메시지 전송 실패")
            print(r.json())


class KoGPT:
    """
    카카오 KoGPT API 클래스

    Parameters
    ----------
    service_key : str
        카카오 개발자 센터에서 발급받은 애플리케이션의 REST API 키
    """

    def __init__(self, service_key=None):
        self.service_key = service_key
        self.headers = {"Authorization": f"KakaoAK {self.service_key}",
                        "Content-Type": "application/json"}
        self.url = "https://api.kakaobrain.com/v1/inference/kogpt/generation"

    def generate(self, prompt, max_tokens, **kwargs):
        """
        문장 생성

        Parameters
        ----------
        prompt : str
            문장 생성에 사용할 문장
        max_tokens : int
            생성할 문장의 최대 길이
        **kwargs : dict
            기타 파라미터

        Returns
        -------
        dict
            생성된 문장
        """
        kwargs['prompt'], kwargs['max_tokens'] = prompt, max_tokens
        try:
            response = requests.post(
                self.url, headers=self.headers, json=kwargs)
            response.json = response.json()
        except Exception as e:
            print("Error")
            print(e)
            return
        return response.json


class DaumSearch:
    """
    카카오 다음 검색 API 클래스

    Parameters
    ----------
    service_key : str
        카카오 개발자 센터에서 발급받은 애플리케이션의 REST API 키
    """

    def __init__(self, service_key=None):
        self.service_key = service_key
        self.headers = {"Authorization": f"KakaoAK {self.service_key}"}
        self.url_dict = {
            "웹문서": "https://dapi.kakao.com/v2/search/web",
            "동영상": "https://dapi.kakao.com/v2/search/vclip",
            "이미지": "https://dapi.kakao.com/v2/search/image",
            "블로그": "https://dapi.kakao.com/v2/search/blog",
            "책": "https://dapi.kakao.com/v3/search/book",
            "카페": "https://dapi.kakao.com/v2/search/cafe",
        }

    def search_web(self, query, dataframe=False, **kwargs):
        """
        웹문서 검색

        Parameters
        ----------
        query : str
            검색어
        dataframe : bool
            True로 설정하면 DataFrame으로 반환, False로 설정하면 dict로 반환, 기본값은 False

        Returns
        -------
        DataFrame or dict
            DataFrame으로 반환하려면 dataframe=True로 설정
        """
        url = self.url_dict.get("웹문서")
        kwargs['query'] = query
        try:
            response = requests.get(url, headers=self.headers, params=kwargs)
            response.raise_for_status()
        except Exception as e:
            print("Request Error")
            print(e)
            return
        try:
            if dataframe:
                return pd.DataFrame(response.json()["documents"])
            else:
                return response.json()
        except Exception as e:
            print("Export Error")
            print(e)
            return

    def search_vclip(self, query, dataframe=False, **kwargs):
        """
        동영상 검색

        Parameters
        ----------
        query : str
            검색어
        dataframe : bool
            True로 설정하면 DataFrame으로 반환, False로 설정하면 dict로 반환, 기본값은 False

        Returns
        -------
        DataFrame or dict
            DataFrame으로 반환하려면 dataframe=True로 설정
        """
        url = self.url_dict.get("동영상")
        kwargs['query'] = query
        try:
            response = requests.get(url, headers=self.headers, params=kwargs)
            response.raise_for_status()
        except Exception as e:
            print("Request Error")
            print(e)
            return
        try:
            if dataframe:
                return pd.DataFrame(response.json()["documents"])
            else:
                return response.json()
        except Exception as e:
            print("Export Error")
            print(e)
            return

    def search_image(self, query, dataframe=False, **kwargs):
        """
        이미지 검색

        Parameters
        ----------
        query : str
            검색어
        dataframe : bool
            True로 설정하면 DataFrame으로 반환, False로 설정하면 dict로 반환, 기본값은 False

        Returns
        -------
        DataFrame or dict
            DataFrame으로 반환하려면 dataframe=True로 설정
        """
        url = self.url_dict.get("이미지")
        kwargs['query'] = query
        try:
            response = requests.get(url, headers=self.headers, params=kwargs)
            response.raise_for_status()
        except Exception as e:
            print("Request Error")
            print(e)
            return
        try:
            if dataframe:
                return pd.DataFrame(response.json()["documents"])
            else:
                return response.json()
        except Exception as e:
            print("Export Error")
            print(e)
            return

    def search_blog(self, query, dataframe=False, **kwargs):
        """
        블로그 검색

        Parameters
        ----------
        query : str
            검색어
        dataframe : bool
            True로 설정하면 DataFrame으로 반환, False로 설정하면 dict로 반환, 기본값은 False

        Returns
        -------
        DataFrame or dict
            DataFrame으로 반환하려면 dataframe=True로 설정
        """
        url = self.url_dict.get("블로그")
        kwargs['query'] = query
        try:
            response = requests.get(url, headers=self.headers, params=kwargs)
            response.raise_for_status()
        except Exception as e:
            print("Request Error")
            print(e)
            return
        try:
            if dataframe:
                return pd.DataFrame(response.json()["documents"])
            else:
                return response.json()
        except Exception as e:
            print("Export Error")
            print(e)
            return

    def search_book(self, query, dataframe=False, **kwargs):
        """
        책 검색

        Parameters
        ----------
        query : str
            검색어
        dataframe : bool
            True로 설정하면 DataFrame으로 반환, False로 설정하면 dict로 반환, 기본값은 False

        Returns
        -------
        DataFrame or dict
            DataFrame으로 반환하려면 dataframe=True로 설정
        """
        url = self.url_dict.get("책")
        kwargs['query'] = query
        try:
            response = requests.get(url, headers=self.headers, params=kwargs)
            response.raise_for_status()
        except Exception as e:
            print("Request Error")
            print(e)
            return
        try:
            if dataframe:
                return pd.DataFrame(response.json()["documents"])
            else:
                return response.json()
        except Exception as e:
            print("Export Error")
            print(e)
            return

    def search_cafe(self, query, dataframe=False, **kwargs):
        """
        카페 검색

        Parameters
        ----------
        query : str
            검색어
        dataframe : bool
            True로 설정하면 DataFrame으로 반환, False로 설정하면 dict로 반환, 기본값은 False

        Returns
        -------
        DataFrame or dict
            DataFrame으로 반환하려면 dataframe=True로 설정
        """
        url = self.url_dict.get("카페")
        kwargs['query'] = query
        try:
            response = requests.get(url, headers=self.headers, params=kwargs)
            response.raise_for_status()
        except Exception as e:
            print("Request Error")
            print(e)
            return
        try:
            if dataframe:
                return pd.DataFrame(response.json()["documents"])
            else:
                return response.json()
        except Exception as e:
            print("Export Error")
            print(e)
            return


class Local:
    """
    카카오 로컬 API 클래스

    Parameters
    ----------
    service_key : str
        카카오 서비스 키
    """

    def __init__(self, service_key=None):
        self.service_key = service_key
        self.headers = {"Authorization": f"KakaoAK {self.service_key}"}
        self.url_dict = {
            "주소 검색하기": "https://dapi.kakao.com/v2/local/search/address.json",
            "좌표로 행정구역정보 받기": "https://dapi.kakao.com/v2/local/geo/coord2regioncode.json",
            "좌표로 주소 변환하기": "https://dapi.kakao.com/v2/local/geo/coord2address.json",
            "좌표계 변환하기": "https://dapi.kakao.com/v2/local/geo/transcoord.json",
            "키워드로 장소 검색하기": "https://dapi.kakao.com/v2/local/search/keyword.json",
            "카테고리로 장소 검색하기": "https://dapi.kakao.com/v2/local/search/category.json",
        }

    def search_address(self, query, dataframe=False, **kwargs):
        """
        주소 검색하기

        Parameters
        ----------
        query : string
            검색을 원하는 질의어
        dataframe : bool
            True로 설정하면 DataFrame으로 반환, False로 설정하면 dict로 반환, 기본값은 False
        **kwargs : dict
            https://developers.kakao.com/docs/latest/ko/local/dev-guide#address-coord 참고

        Returns
        -------
        DataFrame or dict
            DataFrame으로 반환하려면 dataframe=True로 설정
        """
        url = self.url_dict.get("주소 검색하기")
        kwargs['query'] = query
        try:
            response = requests.get(url, headers=self.headers, params=kwargs)
            response.raise_for_status()
        except Exception as e:
            print("Request Error")
            print(e)
            return
        try:
            if dataframe:
                return pd.DataFrame(response.json()["documents"])
            else:
                return response.json()
        except Exception as e:
            print("Export Error")
            print(e)
            return

    def geo_coord2regioncode(self, x, y, dataframe=False, **kwargs):
        """
        좌표로 행정구역정보 받기

        Parameters
        ----------
        x : float
            경도
        y : float
            위도
        dataframe : bool
            True로 설정하면 DataFrame으로 반환, False로 설정하면 dict로 반환, 기본값은 False
        **kwargs : dict
            https://developers.kakao.com/docs/latest/ko/local/dev-guide#coord-to-district 참고

        Returns
        -------
        DataFrame or dict
            DataFrame으로 반환하려면 dataframe=True로 설정
        """
        url = self.url_dict.get("좌표로 행정구역정보 받기")
        kwargs['x'], kwargs['y'] = x, y
        try:
            response = requests.get(url, headers=self.headers, params=kwargs)
            response.raise_for_status()
        except Exception as e:
            print("Request Error")
            print(e)
            return
        try:
            if dataframe:
                return pd.DataFrame(response.json()["documents"])
            else:
                return response.json()
        except Exception as e:
            print("Export Error")
            print(e)
            return

    def geo_coord2address(self, x, y, dataframe=False, **kwargs):
        """
        좌표로 주소 변환하기

        Parameters
        ----------
        x : float
            경도
        y : float
            위도
        dataframe : bool
            True로 설정하면 DataFrame으로 반환, False로 설정하면 dict로 반환, 기본값은 False
        **kwargs : dict
            https://developers.kakao.com/docs/latest/ko/local/dev-guide#coord-to-address 참고

        Returns
        -------
        DataFrame or dict
            DataFrame으로 반환하려면 dataframe=True로 설정
        """
        url = self.url_dict.get("좌표로 주소 변환하기")
        kwargs['x'], kwargs['y'] = x, y
        try:
            response = requests.get(url, headers=self.headers, params=kwargs)
            response.raise_for_status()
        except Exception as e:
            print("Request Error")
            print(e)
            return
        try:
            if dataframe:
                return pd.DataFrame(response.json()["documents"])
            else:
                return response.json()
        except Exception as e:
            print("Export Error")
            print(e)
            return

    def geo_transcoord(self, x, y, output_coord, dataframe=False, **kwargs):
        """
        좌표계 변환하기

        Parameters
        ----------
        x : float
            경도
        y : float
            위도
        output_coord : str
            변환할 좌표계
        dataframe : bool
            True로 설정하면 DataFrame으로 반환, False로 설정하면 dict로 반환, 기본값은 False
        **kwargs : dict
            https://developers.kakao.com/docs/latest/ko/local/dev-guide#trans-coord 참고

        Returns
        -------
        DataFrame or dict
            DataFrame으로 반환하려면 dataframe=True로 설정
        """
        url = self.url_dict.get("좌표계 변환하기")
        kwargs['x'], kwargs['y'], kwargs['output_coord'] = x, y, output_coord
        try:
            response = requests.get(url, headers=self.headers, params=kwargs)
            response.raise_for_status()
        except Exception as e:
            print("Request Error")
            print(e)
            return
        try:
            if dataframe:
                return pd.DataFrame(response.json()["documents"])
            else:
                return response.json()
        except Exception as e:
            print("Export Error")
            print(e)
            return

    def search_keyword(self, query, dataframe=False, **kwargs):
        """
        키워드로 장소 검색하기

        Parameters
        ----------
        query : str
            검색을 원하는 질의어
        dataframe : bool
            True로 설정하면 DataFrame으로 반환, False로 설정하면 dict로 반환, 기본값은 False
        **kwargs : dict
            https://developers.kakao.com/docs/latest/ko/local/dev-guide#search-by-keyword 참고

        Returns
        -------
        DataFrame or dict
            DataFrame으로 반환하려면 dataframe=True로 설정
        """
        url = self.url_dict.get("키워드로 장소 검색하기")
        kwargs['query'] = query
        try:
            response = requests.get(url, headers=self.headers, params=kwargs)
            response.raise_for_status()
        except Exception as e:
            print("Request Error")
            print(e)
            return
        try:
            if dataframe:
                return pd.DataFrame(response.json()["documents"])
            else:
                return response.json()
        except Exception as e:
            print("Export Error")
            print(e)
            return

    def search_category(self, category_group_code, dataframe=False, **kwargs):
        """
        카테고리로 장소 검색하기

        Parameters
        ----------
        category_group_code : str
            카테고리 코드
        dataframe : bool
            True로 설정하면 DataFrame으로 반환, False로 설정하면 dict로 반환, 기본값은 False
        **kwargs : dict
            https://developers.kakao.com/docs/latest/ko/local/dev-guide#search-by-category 참고

        Returns
        -------
        DataFrame or dict
            DataFrame으로 반환하려면 dataframe=True로 설정
        """
        url = self.url_dict.get("카테고리로 장소 검색하기")
        kwargs['category_group_code'] = category_group_code
        try:
            response = requests.get(url, headers=self.headers, params=kwargs)
            response.raise_for_status()
        except Exception as e:
            print("Request Error")
            print(e)
            return
        try:
            if dataframe:
                return pd.DataFrame(response.json()["documents"])
            else:
                return response.json()
        except Exception as e:
            print("Export Error")
            print(e)
            return


class KakaoLocal:
    """ 
    (구) 카카오 로컬 API 클래스

    Parameters
    ----------
    service_key : string
        카카오 개발자 센터에서 발급받은 애플리케이션의 REST API 키
    """

    def __init__(self, service_key=None):

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
