import requests, xmltodict, json
from bs4 import BeautifulSoup

class CoronaVo:
    def __init__(self, stdDay=None, deathCnt=None, incDec=None, isolClearCnt=None, isolIngCnt=None,
                 gubun=None, localOccCnt=None, defcnt=None, overFlowCnt=None):

        self.stdDay = stdDay #기준일
        self.deathCnt = deathCnt #지금까지 사망자 수
        self.incDec = incDec #전일대비 증감수
        self.isolClearCnt = isolClearCnt #격리 해제 수
        self.isolIngCnt = isolIngCnt # 격리중 환자수
        self.gubun = gubun #시군구
        self.localOccCnt = localOccCnt #지역발생 수
        self.defcnt = defcnt #현재까지 확진자 수
        self.overFlowCnt = overFlowCnt #해외유입 수


class CoronaGraph:
    def __init__(self, incDec, gubun):
        self.incDec = incDec
        self.gubun = gubun

    def __str__(self):
        return self.gubun+': '+ self.incDec


class CoronaService:
    def __init__(self):
        self.url = 'http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19SidoInfStateJson?serviceKey=%s&pageNo=1&numOfRows=10&startCreateDt=%s&endCreateDt=%s'
        self.apiKey = '4tdDtEO6U6Iu3LUIgh5CaYYiZfUj9XrwBjOpicIiJxWHmGWOQbO8Pr9q8R8kNeptActfQZHmfho%2BT2Euxcn2zQ%3D%3D'
        self.sd = 20210724
        self.ed = 20210724

    def getCoronaAll(self):
        url = self.url%(self.apiKey, self.sd, self.ed)
        print(url)
        html = requests.get(url).text
        root = BeautifulSoup(html, 'lxml-xml')
        code = root.find('resultCode').get_text()
        msg = root.find('resultMsg').get_text()
        print('처리결과:', msg)
        if code == '0':
            stdDay = root.find('stdDay').get_text()
            deathCnt = root.find('deathCnt').get_text()
            incDec = root.find('incDec').get_text()
            isolClearCnt = root.find('isolClearCnt').get_text()
            isolIngCnt = root.find('isolIngCnt').get_text()
            gubun = root.find('gubun').get_text()
            localOccCnt = root.find('localOccCnt').get_text()
            defcnt = root.find('defcnt').get_text()
            overFlowCnt = root.find('overFlowCnt').get_text()

            return CoronaVo(stdDay, deathCnt, incDec, isolClearCnt, isolIngCnt, gubun, localOccCnt, defcnt, overFlowCnt)
        else:
            return msg

    def getCoronaGraph(self):
        url = self.url%(self.apiKey, self.sd, self.ed)
        print(url)
        html = requests.get(url).text
        root = BeautifulSoup(html, 'lxml-xml')
        code = root.find('resultCode').get_text()
        msg = root.find('resultMsg').get_text()
        print('처리결과:', msg)
        self.gubun = '합계'
        corona = []
        if code=='00':
            items = root.select('item')

            for item in items:
                incDec = item.find('incDec').get_text()
                gubun = item.find('gubun').get_text()
                print(incDec, gubun)
                corona.append(CoronaGraph(incDec, gubun))
            print(corona)
            return corona
        else:
            return msg

    def getCoronaGraph2(self):
        api_key = '4tdDtEO6U6Iu3LUIgh5CaYYiZfUj9XrwBjOpicIiJxWHmGWOQbO8Pr9q8R8kNeptActfQZHmfho%2BT2Euxcn2zQ%3D%3D'
        sd = 20210724
        ed = 20210724
        url = 'http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19SidoInfStateJson?serviceKey=%s&pageNo=0&numOfRows=1&startCreateDt=%s&endCreateDt=%s' % (
        api_key, sd, ed)
        content = requests.get(url).content
        dict = xmltodict.parse(content)
        jsonString = json.dumps(dict['response']['body'], ensure_ascii=False)
        jsonObj = json.loads(jsonString)
        lst = []
        for item in jsonObj['items']['item']:
            c = CoronaGraph(item['incDec'], item['gubun'])
            lst.append(c)
        print(lst)
        return lst

if __name__ == "__main__" :
    a = CoronaService()
    a.getCoronaGraph()

