from flask import Blueprint, request, redirect, render_template, session
import tour.models.board as b

bp = Blueprint("board", __name__, url_prefix = "/board")
board_service = b.cBoard_service()

@bp.route("/")
def board() :
    bd = board_service.Get_all()
    page = request.args.get("page", 1, int)
    return render_template("/board/board_form.html", bd = bd, page = page)

@bp.route("/insert")
def insert_form() :
    return render_template("/board/insert_form.html")

@bp.route("/insert", methods = ["POST"])
def insert() :
    loc = request.form["loc"]
    title = request.form["title"]
    content = request.form["content"]
    img_path = request.form["img_path"]
    bd = b.cBoard(writer = session["name"], title = title, content = content, img_path = img_path, email = session["id"], loc = loc)
    board_service.Add_board(bd)
    return redirect("/board/")

@bp.route("/detail")
def detail() :
    num = request.args.get("num", 0, int)
    bd = board_service.Get_board_num(num)
    return render_template("/board/detail.html", bd = bd)

@bp.route("/search", methods=["POST"])
def search() :
    option = request.form["option"]
    val = request.form["word"]
    bd = board_service.Get_board(option, val)
    return render_template("/board/board_form.html", bd=bd, page = 1)