import pymysql, requests
from bs4 import BeautifulSoup

class Location:     #location 테이블
    def __init__(self, area_code=None, area_name=None, sigungu_code=None, cat1=None, cat2=None, cat3=None, count=None):
        self.area_code = area_code
        self.area_name = area_name
        self.sigungu_code = sigungu_code
        self.cat1 = cat1
        self.cat2 = cat2
        self.cat3 = cat3
        self.count = count

class AreaCodeVo:
    def __init__(self, code=None, name=None, rnum=None):
        self.code = code
        self.name = name
        self.rnum = rnum

class AreaBasedVo:
    def __init__(self, addr1=None, areacode=None, cat1=None, cat2=None, cat3=None, contentid=None,
                 contenttypeid=None, createdtime=None, firstimage=None, firstimage2=None, mapx=None, mapy=None,
                 mlevel=None, modifiedtime=None, readcount=None, sigungucode=None, title=None, zipcode=None):
        self.addr1 = addr1
        self.areacode = areacode
        self.cat1 = cat1
        self.cat2 = cat2
        self.cat3 = cat3
        self.contentid = contentid
        self.contenttypeid = contenttypeid
        self.createdtime = createdtime
        self.firstimage = firstimage
        self.firstimage2 = firstimage2
        self.mapx = mapx
        self.mapy = mapy
        self.mlevel = mlevel
        self.modifiedtime = modifiedtime
        self.readcount = readcount
        self.sigungucode = sigungucode
        self.title = title
        self.zipcode = zipcode
'''
areaBasedList
<addr1>경상북도 성주군 수륜면 가야산식물원길 49</addr1>
<areacode>35</areacode>
<cat1>A01</cat1>
<cat2>A0101</cat2>
<cat3>A01010700</cat3>
<contentid>129212</contentid>
<contenttypeid>12</contenttypeid>
<createdtime>20060828000000</createdtime>
<firstimage>http://tong.visitkorea.or.kr/cms/resource/70/1399670_image2_1.jpg</firstimage>
<firstimage2>http://tong.visitkorea.or.kr/cms/resource/70/1399670_image3_1.jpg</firstimage2>
<mapx>128.1418573045</mapx>
<mapy>35.8031276100</mapy>
<mlevel>6</mlevel>
<modifiedtime>20210524165843</modifiedtime>
<readcount>43000</readcount>
<sigungucode>10</sigungucode>
<title>가야산 야생화식물원</title>
<zipcode>40063</zipcode>
'''

class AreaService:
    def __init__(self):
        self.url = 'http://api.visitkorea.or.kr/openapi/service/rest/KorWithService/%s?ServiceKey=%s&%s=%s&MobileOS=ETC&MobileApp=TestApp'
        #페이지 포함한 url
        self.page_url = 'http://api.visitkorea.or.kr/openapi/service/rest/KorWithService/%s?ServiceKey=%s&%s=%s&%s=%s&MobileOS=ETC&MobileApp=TestApp'
        self.apiKey = '4tdDtEO6U6Iu3LUIgh5CaYYiZfUj9XrwBjOpicIiJxWHmGWOQbO8Pr9q8R8kNeptActfQZHmfho%2BT2Euxcn2zQ%3D%3D'
#http://api.visitkorea.or.kr/openapi/service/rest/KorWithService/areaCode?ServiceKey=4tdDtEO6U6Iu3LUIgh5CaYYiZfUj9XrwBjOpicIiJxWHmGWOQbO8Pr9q8R8kNeptActfQZHmfho%2BT2Euxcn2zQ%3D%3D&numOfRows=10&pageNo=1&MobileOS=ETC&MobileApp=TestApp
    def areaCode(self, numOfRows, pageNo):
        url = self.page_url%('areaCode', self.apiKey, 'numOfRows', numOfRows, 'pageNo', pageNo) # 한 페이지에 출력할 데이터 개수
        html = requests.get(url).text
        root = BeautifulSoup(html, 'lxml-xml')  # 파서의 종류를 xml로 지정
        code = root.find('resultCode').get_text()
        msg = root.find('resultMsg').get_text()
        print('url:', url)
        print('처리결과:', msg)

        vo_list = []
        if code =='0000':
            items = root.select('item')
            try:
                for item in items:
                    code = item.find('code').get_text()
                    name = item.find('name').get_text()
                    rnum = item.find('rnum').get_text()
                    vo_list.append(AreaCodeVo(code=code, name=name, rnum=rnum))
            except Exception as e:
                print(e)
            finally:
                return vo_list



    def areaBasedList(self, areaCode):
        url = self.url%('areaBasedList', self.apiKey, 'areaCode', areaCode) # 한 페이지에 출력할 데이터 개수
        html = requests.get(url).text
        root = BeautifulSoup(html, 'lxml-xml')  # 파서의 종류를 xml로 지정
        code = root.find('resultCode').get_text()
        msg = root.find('resultMsg').get_text()
        print('처리결과:', msg)

        vo_list = []
        if code =='0000':
            items = root.select('item')
            try:
                for item in items:
                    addr1 = item.find('addr1').get_text()
                    areacode = item.find('areacode').get_text()
                    contentid = item.find('contentid').get_text()
                    title = item.find('title').get_text()
                    firstimage = item.find('firstimage').get_text()
                    firstimage2 = item.find('firstimage2').get_text()
                    sigungucode = item.find('sigungucode').get_text()
                    vo_list.append(AreaBasedVo(areacode=areacode, addr1=addr1, contentid=contentid, title=title,
                                               firstimage=firstimage, firstimage2=firstimage2,
                                               sigungucode=sigungucode))
            except Exception as e:
                print(e)
            finally:
                return vo_list

