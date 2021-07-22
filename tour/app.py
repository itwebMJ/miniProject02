from flask import Flask, request, render_template
import routes.location_route as rl


app = Flask(__name__, template_folder="templates")
app.secret_key = "cggasadfsgadf" #시크릿키 설정

#생성한 블루프린트 등록
app.register_blueprint(rl.bp)


@app.route('/')
def root():
    return render_template('index.html')


if __name__ == '__main__':
    app.debug=True
    app.run()#flask 서버 실행