from flask import Flask, request, render_template
import routes.location_route as rl
import routes.coronainfo_route as corona
import routes.member_route as mr
import routes.board_route as br
import models.board as b


app = Flask(__name__, template_folder="templates")
app.secret_key = "cggasadfsgadf" #시크릿키 설정

#생성한 블루프린트 등록
app.register_blueprint(rl.bp)
app.register_blueprint(corona.bp)
app.register_blueprint(mr.bp)
app.register_blueprint(br.bp)
board_service = b.cBoard_service()

@app.route('/')
def home() :
    bd = board_service.Get_all()
    return render_template("/index.html", bd = bd)

if __name__ == '__main__':
    app.debug=True
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run()#flask 서버 실행