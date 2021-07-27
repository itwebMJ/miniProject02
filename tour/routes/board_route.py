from flask import Blueprint, request, redirect, render_template, session
import tour.models.board as b
import tour.models.reboard as rb

bp = Blueprint("board", __name__, url_prefix = "/board")
board_service = b.cBoard_service()
reboard_service = rb.cReboard_service()

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

    bd = b.cBoard(writer = session["name"], title = title, content = content, email = session["id"], loc = loc)
    board_service.Add_board(bd)
    return redirect("/board/")

@bp.route("/detail")
def detail() :
    num = request.args.get("num", 0, int)
    bd = board_service.Get_board_num(num)
    content = bd.content.split("<br>")
    rebd = reboard_service.Get_reboard(num)
    for idx, i in enumerate(rebd) :
        rebd[idx].content = i.content.replace('<br>', '\n')
    return render_template("/board/detail.html", bd = bd, content = content, rebd = rebd)

@bp.route("/search", methods=["POST"])
def search() :
    option = request.form["option"]
    val = request.form["word"]
    bd = board_service.Get_board(option, val)
    return render_template("/board/board_form.html", bd=bd, page = 1)

@bp.route("/delete", methods=["POST"])
def delete() :
    num = request.form["num"]
    board_service.Delete_board(num)
    return redirect("/board/")

@bp.route("/edit", methods=["POST"])
def edit_form() :
    num = request.form["num"]
    bd = board_service.Get_board_num(num)
    content = bd.content.replace('<br>', '\n')
    return render_template("/board/edit_form.html", bd = bd, content = content)

@bp.route("/update", methods=["POST"])
def update() :
    num = request.form["num"]
    title = request.form["title"]
    loc = request.form["loc"]
    content = request.form["content"]
    bd = b.cBoard(num = num, title = title, loc = loc, content = content)
    board_service.Edit_board(bd)
    return redirect("/board/detail?num=" + str(num))

@bp.route("/reboard", methods = ["POST"])
def reboard() :
    num = request.form["num"]
    writer = session["name"]
    email = session["id"]
    content = request.form["content"]
    reboard_service.Add_reboard(rb.cReboard(num = num, writer = writer, email = email, content = content))
    return redirect("/board/detail?num=" + str(num))

@bp.route("/redelete", methods = ["POST"])
def redelete() :
    pk = request.form["num"]
    num = request.form["bdnum"]
    reboard_service.Delete_reboard(pk)
    return redirect("/board/detail?num=" + str(num))

@bp.route("/reedit", methods = ["POST"])
def reedit() :
    pk = request.form["num"]
    num = request.form["bdnum"]
    rebd = reboard_service.Get_reboard(num)
    bd = board_service.Get_board_num(num)
    content = bd.content.split("<br>")
    for idx, i in enumerate(rebd) :
        rebd[idx].content = i.content.replace('<br>', '\n')
    return render_template("/board/reedit.html", pk = int(pk), rebd = rebd, bd = bd, content = content)

@bp.route("/editreboard", methods = ["POST"])
def editreboard() :
    pk = request.form["pk"]
    num = request.form["num"]
    content = request.form["content"]
    reboard_service.Edit_reboard(rb.cReboard(pk = pk, content = content))
    return redirect("/board/detail?num=" + str(num))