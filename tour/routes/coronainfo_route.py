from flask import Blueprint, render_template, request
import tour.models.coronainfo as corona
import matplotlib.pyplot as plt

bp = Blueprint('coronainfo', __name__, url_prefix='/coronainfo')
coronaService = corona.CoronaService()

@bp.route('/')
def coronaGraph():
    c = coronaService.getCoronaGraph()
    img_path = 'static/graph/my_plot.png'
    plt.rcParams['font.family'] = 'Malgun Gothic'
    plt.rcParams['axes.unicode_minus'] = False
    x = [c[i].gubun for i in range(len(c))]
    y = [c[i].incDec for i in range(len(c))]
    print(x)
    fig, ax = plt.subplots()
    plt.bar(x, y)
    plt.bar(x, y, color='slategrey')
    plt.rcParams['figure.figsize'] = [15, 5]
    plt.xticks(rotation=0)
    plt.xlabel('코로나 발생 지역')
    plt.ylabel('코로나 확진자 수')
    '''
    plt.hist(x, bins=15)    
    '''

    fig.savefig(img_path)
    img_path = '/' + img_path

    co_lst = coronaService.getCoronaGraph()
    list_loc = ['서울', '경기', '부산', '대구', '광주', '인천', '울산', '강원', '충북', '충남', '경북', '경남', '전북', '전남', '제주']

    return render_template('coronainfo/fpage.html', img_path = img_path, co_lst=co_lst, list_loc=list_loc)

@bp.route('/corouteGubun-all')
def CoRouteGubun():
    city = request.args.get("city", '', str)
    c = coronaService.getCoronaGubun(city)
    print(city)
    return render_template('coronainfo/detail.html', c=c)















