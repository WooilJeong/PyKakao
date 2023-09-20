import io
import json
import base64
import urllib
import requests
import pandas as pd
from PIL import Image


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

    def get_url_for_generating_code(self):
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


class Karlo:
    """
    카카오 Karlo API 클래스

    Parameters
    ----------
    service_key : str
        카카오 개발자 센터에서 발급받은 애플리케이션의 REST API 키
    """

    def __init__(self, service_key=None):
        self.service_key = service_key
        self.headers = {
            "Authorization": f"KakaoAK {self.service_key}",
            "Content-Type": "application/json",
        }

    def text_to_image(
        self, 
        prompt, 
        negative_prompt=None, 
        width=512, 
        height=512, 
        upscale=None, 
        scale=2, 
        image_format="webp", 
        image_quality=70, 
        samples=1, 
        return_type="url", 
        prior_num_inference_steps=25, 
        prior_guidance_scale=5.0, 
        num_inference_steps=50, 
        guidance_scale=5.0, 
        scheduler="decoder_ddim_v_prediction", 
        seed=None, 
        nsfw_checker=False
    ):
        """
        이미지 생성하기 API

        Parameters
        ----------
        prompt : str
            이미지를 묘사하는 제시어, 영문만 지원 (최대: 256자)
        ... (다른 파라미터들)

        Returns
        -------
        dict
            생성된 이미지의 정보
        """
        _url = "https://api.kakaobrain.com/v2/inference/karlo/t2i"
        _json = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "width": width,
            "height": height,
            "upscale": upscale,
            "scale": scale,
            "image_format": image_format,
            "image_quality": image_quality,
            "samples": samples,
            "return_type": return_type,
            "prior_num_inference_steps": prior_num_inference_steps,
            "prior_guidance_scale": prior_guidance_scale,
            "num_inference_steps": num_inference_steps,
            "guidance_scale": guidance_scale,
            "scheduler": scheduler,
            "seed": seed,
            "nsfw_checker": nsfw_checker
        }
        _json = {k: v for k, v in _json.items() if v is not None}
        return requests.post(_url, json=_json, headers=self.headers).json()
    
    def upscale_image(
        self, 
        images, 
        scale=2, 
        image_format="webp", 
        image_quality=70, 
        return_type="url"
    ):
        """
        이미지 확대하기 API

        Parameters
        ----------
        images : list of str
            확대할 이미지 파일을 Base64 인코딩한 값들의 리스트
        scale : int, optional
            확대 배율, 2 또는 4 중 하나 (기본값: 2)
        image_format : str, optional
            이미지 파일 형식, "webp", "jpeg", "png" 중 하나 (기본값: "webp")
        image_quality : int, optional
            이미지 저장 품질 (기본값: 70, 최소: 1, 최대: 100)
        return_type : str, optional
            응답의 이미지 파일 반환 형식, "base64_string" 또는 "url" 중 하나 (기본값: "url")

        Returns
        -------
        dict
            확대된 이미지의 정보
        """
        _url = "https://api.kakaobrain.com/v2/inference/karlo/upscale"
        _json = {
            "images": images,
            "scale": scale,
            "image_format": image_format,
            "image_quality": image_quality,
            "return_type": return_type
        }
        _json = {k: v for k, v in _json.items() if v is not None}
        return requests.post(_url, json=_json, headers=self.headers).json()

    def transform_image(
        self, 
        image,
        prompt=None,
        negative_prompt=None,
        width=512,
        height=512,
        upscale=None,
        scale=2,
        image_format="webp",
        image_quality=70,
        samples=1,
        return_type="url",
        num_inference_steps=50,
        guidance_scale=5.0,
        scheduler="decoder_ddim_v_prediction",
        seed=None,
        nsfw_checker=False
    ):
        """
        이미지 변환하기 API

        Parameters
        ----------
        image : str
            원본 이미지 파일을 Base64 인코딩한 값
        ... (다른 파라미터들)

        Returns
        -------
        dict
            생성된 이미지의 정보
        """
        _url = "https://api.kakaobrain.com/v2/inference/karlo/variations"
        _json = {
            "image": image,
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "width": width,
            "height": height,
            "upscale": upscale,
            "scale": scale,
            "image_format": image_format,
            "image_quality": image_quality,
            "samples": samples,
            "return_type": return_type,
            "num_inference_steps": num_inference_steps,
            "guidance_scale": guidance_scale,
            "scheduler": scheduler,
            "seed": seed,
            "nsfw_checker": nsfw_checker
        }
        _json = {k: v for k, v in _json.items() if v is not None}
        return requests.post(_url, json=_json, headers=self.headers).json()

    def check_nsfw(self, images):
        """
        NSFW 검사하기 API

        Parameters
        ----------
        images : list of str
            검사 대상 이미지 파일을 Base64 인코딩한 값들의 리스트

        Returns
        -------
        dict
            NSFW 검사 결과
        """
        _url = "https://api.kakaobrain.com/v2/inference/karlo/nsfw_checker"
        _json = {
            "images": images
        }
        return requests.post(_url, json=_json, headers=self.headers).json()

    def get_first_image_from_response(self, response):
        """
        응답에서 첫 번째 이미지를 가져와서 Image 객체로 반환하는 함수

        Parameters
        ----------
        response : dict
            t2i API의 응답 결과

        Returns
        -------
        Image
            첫 번째 이미지에 대한 Image 객체
        """
        try:
            images = response.get('images')
            if not images:
                print("Error: 'images' key not found in the response.")
                return None

            first_image = images[0]
            if isinstance(first_image, dict) and 'image' in first_image:
                image_url = first_image.get('image')
            else:
                image_url = first_image

            return Image.open(urllib.request.urlopen(image_url))

        except IndexError:
            print("Error: 'images' list is empty.")
        except TypeError:
            print("Error: Unexpected type for 'images' or its content.")
        except Exception as e:
            print(f"Unexpected error occurred: {e}")

        return None
    
    def string_to_image(self, base64_string, mode='RGBA'):
        """
        base64 string을 이미지로 변환

        Parameters
        ----------
        base64_string : str
            base64 string
        mode : str, optional
            이미지 모드(기본값: RGBA)

        Returns
        -------
        PIL.Image
            이미지
        """
        return Image.open(io.BytesIO(base64.b64decode(str(base64_string)))).convert(mode)

    def image_to_string(self, img):
        """
        이미지를 base64 string으로 변환

        Parameters
        ----------
        img : PIL.Image
            이미지

        Returns
        -------
        str
            base64 string
        """
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        my_encoded_img = base64.encodebytes(
            img_byte_arr.getvalue()).decode('ascii')
        return my_encoded_img


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


class _Karlo:
    """
    (Deprecated)
    카카오 Karlo API 클래스

    Parameters
    ----------
    service_key : str
        카카오 개발자 센터에서 발급받은 애플리케이션의 REST API 키
    """

    def __init__(self, service_key=None):
        self.service_key = service_key
        self.headers = {"Authorization": f"KakaoAK {self.service_key}",
                        "Content-Type": "application/json"}

    def text_to_image(self, text, batch_size=1):
        """
        이미지 생성하기 API

        Parameters
        ----------
        text : str
            생성할 이미지를 묘사하는 제시어, 영문만 지원(최대: 256자)
            참고: 
            - 활용 가이드(https://developers.kakao.com/docs/latest/ko/karlo/how-to-use)
        batch_size : int, optional
            생성할 이미지 수(기본값: 1, 최대: 8)

        Returns
        -------
        dict
            생성된 이미지의 정보
        """
        _url = "https://api.kakaobrain.com/v1/inference/karlo/t2i"
        _json = {
            "prompt": {
                "text": text,
                "batch_size": batch_size,
            }
        }
        return requests.post(_url, json=_json, headers=self.headers).json()

    def transform_image(self, image, batch_size=1):
        """
        이미지 변환하기

        Parameters
        ----------
        image : str
            변환할 원본 이미지를 Base64 인코딩한 값
            참고: 
            - 이미지 파일 규격(https://developers.kakao.com/docs/latest/ko/karlo/rest-api#before-you-begin-image-requirement)
            - 이미지 인코딩 및 디코딩(https://developers.kakao.com/docs/latest/ko/karlo/rest-api#before-you-begin-encode-and-decode)
        batch_size : int, optional
            생성할 이미지 수(기본값: 1, 최대: 8)

        Returns
        -------
        dict
            생성된 이미지의 정보
        """
        _url = "https://api.kakaobrain.com/v1/inference/karlo/variations"
        _json = {
            "prompt": {
                "image": image,
                "batch_size": batch_size,
            }
        }
        return requests.post(_url, json=_json, headers=self.headers).json()

    def inpaint_image(self, image, mask, text="", batch_size=1):
        """
        이미지 편집하기

        Parameters
        ----------
        image : str
            원본 이미지를 Base64 인코딩한 값
            참고:
            - 이미지 파일 규격(https://developers.kakao.com/docs/latest/ko/karlo/rest-api#before-you-begin-image-requirement)
            - 이미지 인코딩 및 디코딩(https://developers.kakao.com/docs/latest/ko/karlo/rest-api#before-you-begin-encode-and-decode)
        mask : str
            편집할 부분을 표시한 원본 이미지를 Base64 인코딩한 값
            편집할 부분을 검은색(Grayscale, RGB 기준 0)으로 가려서 표시
            이미지의 여러 곳 마스킹 가능
            참고:
            - 이미지 파일 규격(https://developers.kakao.com/docs/latest/ko/karlo/rest-api#before-you-begin-image-requirement)
            - 이미지 인코딩 및 디코딩(https://developers.kakao.com/docs/latest/ko/karlo/rest-api#before-you-begin-encode-and-decode)  
        text : str, optional
            편집해 넣을 이미지를 묘사하는 제시어, 영문만 지원(최대: 256자)
            text 값이 설정되지 않으면 편집할 부분의 주변과 어울리도록 사물을 삭제하거나 대체함
            (기본값: "", 빈 문자열)
            참고:
            - 활용 가이드(https://developers.kakao.com/docs/latest/ko/karlo/how-to-use)
        batch_size : int, optional
            생성할 이미지 수(기본값: 1, 최대: 8)

        Returns
        -------
        dict
            생성된 이미지의 정보
        """
        _url = "https://api.kakaobrain.com/v1/inference/karlo/inpainting"
        _json = {
            "prompt": {
                "image": image,
                "mask": mask,
                "text": text,
                "batch_size": batch_size,
            }
        }
        return requests.post(_url, json=_json, headers=self.headers).json()

    def string_to_image(self, base64_string, mode='RGBA'):
        """
        base64 string을 이미지로 변환

        Parameters
        ----------
        base64_string : str
            base64 string
        mode : str, optional
            이미지 모드(기본값: RGBA)

        Returns
        -------
        PIL.Image
            이미지
        """
        return Image.open(io.BytesIO(base64.b64decode(str(base64_string)))).convert(mode)

    def image_to_string(self, img):
        """
        이미지를 base64 string으로 변환

        Parameters
        ----------
        img : PIL.Image
            이미지

        Returns
        -------
        str
            base64 string
        """
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        my_encoded_img = base64.encodebytes(
            img_byte_arr.getvalue()).decode('ascii')
        return my_encoded_img

