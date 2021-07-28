import requests, xmltodict, json
from bs4 import BeautifulSoup
from datetime import date

class CoronaVo:
    def __init__(self, stdDay=None, deathCnt=None, incDec=None, isolClearCnt=None, isolIngCnt=None,
                 gubun=None, localOccCnt=None, defCnt=None, overFlowCnt=None):

        self.stdDay = stdDay #기준일
        self.deathCnt = deathCnt #지금까지 사망자 수
        self.incDec = incDec #전일대비 증감수
        self.isolClearCnt = isolClearCnt #격리 해제 수
        self.isolIngCnt = isolIngCnt # 격리중 환자수
        self.gubun = gubun #시군구
        self.localOccCnt = localOccCnt #지역발생 수
        self.defCnt = defCnt #현재까지 확진자 수
        self.overFlowCnt = overFlowCnt #해외유입 수

    def __str__(self):
        return self.gubun + ': ' + self.stdDay+'/'+self.incDec+'/'+self.localOccCnt+'/'+self.overFlowCnt\
               +'/'+self.isolIngCnt+'/'+self.defCnt+'/'+self.isolIngCnt+'/'+self.deathCnt

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
        # sd = str(date.today())
        # day_str = sd.split('-')[0]+sd.split('-')[1]+sd.split('-')[2]
        # self.sd = int(day_str)
        # self.ed = int(day_str)
        self.sd = 20210727
        self.ed = 20210727

    def getCoronaAll(self):
        url = self.url%(self.apiKey, self.sd, self.ed)
        print(url)
        html = requests.get(url).text
        root = BeautifulSoup(html, 'lxml-xml')
        code = root.find('resultCode').get_text()
        msg = root.find('resultMsg').get_text()
        print('처리결과:', msg)
        if code == '00':
            stdDay = root.find('stdDay').get_text()
            deathCnt = root.find('deathCnt').get_text()
            incDec = root.find('incDec').get_text()
            isolClearCnt = root.find('isolClearCnt').get_text()
            isolIngCnt = root.find('isolIngCnt').get_text()
            gubun = root.find('gubun').get_text()
            localOccCnt = root.find('localOccCnt').get_text()
            defCnt = root.find('defCnt').get_text()
            overFlowCnt = root.find('overFlowCnt').get_text()

            return CoronaVo(stdDay=stdDay, deathCnt=deathCnt, incDec=incDec,
                            isolClearCnt=isolClearCnt, isolIngCnt=isolIngCnt,
                            gubun=gubun, localOccCnt=localOccCnt, defCnt=defCnt, overFlowCnt=overFlowCnt)
        else:
            return msg

    def getCoronaGraph(self):
        url = self.url%(self.apiKey, self.sd, self.ed)
        print(url)
        html = requests.get(url).text
        root = BeautifulSoup(html, 'lxml-xml')
        code = root.find('resultCode').get_text()
        msg = root.find('resultMsg').get_text()
        print(code)
        print('처리결과:', msg)
        self.gubun = '합계'
        corona = []
        if code=='00':
            items = root.select('item')

            for item in items:
                incDec = item.find('incDec').get_text()
                gubun = item.find('gubun').get_text()
                corona.append(CoronaGraph(incDec=incDec, gubun=gubun))
            return corona
        else:
            return msg

    def getCoronaGubun(self, city=None):
        url = self.url%(self.apiKey, self.sd, self.ed)
        print(url)
        html = requests.get(url).text
        root = BeautifulSoup(html, 'lxml-xml')
        code = root.find('resultCode').get_text()
        msg = root.find('resultMsg').get_text()
        print(code)
        print('처리결과:', msg)
        if code == '00':
            items = root.select('item')

            for item in items:
                gubun = item.find('gubun').get_text()
                if city==gubun:
                    stdDay = item.find('stdDay').get_text()
                    incDec = item.find('incDec').get_text()
                    localOccCnt = item.find('localOccCnt').get_text()
                    overFlowCnt = item.find('overFlowCnt').get_text()
                    defCnt = item.find('defCnt').get_text()
                    deathCnt = item.find('deathCnt').get_text()
                    isolClearCnt = item.find('isolClearCnt').get_text()
                    isolIngCnt = item.find('isolIngCnt').get_text()

                    return CoronaVo(gubun=gubun, stdDay=stdDay, incDec=incDec, localOccCnt=localOccCnt,
                                    overFlowCnt=overFlowCnt, defCnt=defCnt, deathCnt=deathCnt, isolClearCnt=isolClearCnt, isolIngCnt=isolIngCnt)
        else:
            return msg


    '''
    def getCoronaGraph2(self):
        api_key = '4tdDtEO6U6Iu3LUIgh5CaYYiZfUj9XrwBjOpicIiJxWHmGWOQbO8Pr9q8R8kNeptActfQZHmfho%2BT2Euxcn2zQ%3D%3D'
        sd = 20210725
        ed = 20210725
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
    
'''

