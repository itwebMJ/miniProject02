from flask import Blueprint, render_template, request, redirect, session
import tour.models.member as m

bp = Blueprint("member", __name__, url_prefix = "/member")
member_service = m.cMember_service()

@bp.route('/')
def login_form() :
    mem = member_service.Get_all()
    meminfo_lst = []
    for i in mem:
        lst = []
        lst.append(i.email)
        lst.append(i.pwd)
        meminfo_lst.append(lst)

    return render_template("/member/login.html", mem = meminfo_lst)

@bp.route('/insert')
def insert_form() :
    mem = member_service.Get_all()
    email_lst = []
    for i in mem :
        email_lst.append(i.email)
    return render_template("/member/insert.html", mem = email_lst)

@bp.route("/insert", methods = ["POST"])
def insert() :
    id = request.form["id"]
    pwd = request.form["pwd"]
    name = request.form["name"]
    member_service.Add_member(m.cMember(email = id, pwd = pwd, name = name))
    return redirect("/member/")

@bp.route("/login", methods = ["POST"])
def login() :
    session["id"] = request.form["id"]
    mem = member_service.Get_member(session["id"])
    session["name"] = mem.name
    return redirect("/")

@bp.route("/logout")
def logout() :
    session.pop("id", None)
    return redirect('/')
