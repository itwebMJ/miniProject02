from flask import Flask, render_template
import routes.location_route as rl
import routes.coronainfo_route as corona
import routes.member_route as mr
import routes.board_route as br
import tour.models.board as b
import tour.models.coronainfo as c_info
import tour.models.location as loc

app = Flask(__name__, template_folder="templates")

#생성한 블루프린트 등록
app.register_blueprint(rl.bp)
app.register_blueprint(corona.bp)
app.register_blueprint(mr.bp)
app.register_blueprint(br.bp)
board_service = b.cBoard_service()
coronainfo_service = c_info.CoronaService()
areaService = loc.AreaService()

@app.route('/')
def home() :
    bd = board_service.Get_all()
    coronainfo = coronainfo_service.getCoronaGraph()
    areaList1 = areaService.searchKeyword(coronainfo[1].gubun, 5, 1)
    areaList2 = areaService.searchKeyword(coronainfo[2].gubun, 5, 1)
    areaList3 = areaService.searchKeyword(coronainfo[3].gubun, 5, 1)
    coronainfo1 = coronainfo_service.getCoronaGubun(coronainfo[1].gubun)
    coronainfo2 = coronainfo_service.getCoronaGubun(coronainfo[2].gubun)
    coronainfo3 = coronainfo_service.getCoronaGubun(coronainfo[3].gubun)
    return render_template("/index.html", bd = bd, areaList1=areaList1[0],
                           areaList2=areaList2[0], areaList3=areaList3[0],
                           coronainfo1 = coronainfo1, coronainfo2 = coronainfo2, coronainfo3 = coronainfo3)

if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run()#flask 서버 실행