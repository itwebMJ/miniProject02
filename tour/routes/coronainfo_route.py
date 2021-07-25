from flask import Blueprint, render_template, request, redirect, session
import tour.models.coronainfo as corona
import matplotlib.pyplot as plt

bp = Blueprint('coronainfo', __name__, url_prefix='/coronainfo')
coronaService = corona.CoronaService()

@bp.route('/')
def corona():
    c = coronaService.getCoronaGraph()
    img_path = 'static/graph/my_plot.png'
    x = [c[i].gubun for i in range(len(c))]
    y = [c[i].incDec for i in range(len(c))]
    print(x)
    fig, ax = plt.subplots()
    plt.plot(x, y)
    fig.savefig(img_path)
    img_path = '/' + img_path
    return render_template('coronainfo/fpage.html', img_path = img_path)

@bp.route('/coronaGraph')
def coronaGraph():
    img_path = 'static/graph/my_plot.png'
    c = coronaService.getCoronaGraph2()
    x = request.form[c('gubun')]
    y = request.form[c('incDec')]

    fig, ax = plt.subplots()
    plt.plot(x, y)

    fig.savefig(img_path)
    img_path = '/' + img_path


    return render_template('coronainfo/fpage.html', c=c, img_path=img_path)













