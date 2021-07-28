from flask import Blueprint, render_template, request, redirect, session
import tour.models.member as m
import matplotlib.pyplot as plt


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
    session["interest"] = mem.interest
    return redirect("/")

@bp.route("/logout")
def logout() :
    session.pop("id", None)
    session.pop("name", None)
    session.pop("interest", None)
    return redirect('/')

@bp.route("/loc")
def loc() :
    # plt.rc('font', family='D2Coding')
    plt.rcParams['font.family'] = 'Malgun Gothic'
    plt.rcParams['axes.unicode_minus'] = False
    location = {"서울특별시":(290, 860), "인천광역시":(210, 880), "대전광역시":(350, 660), "대구광역시":(540, 570), "광주광역시":(240, 420),
                "부산광역시":(640, 420), "울산광역시":(670, 510), "세종특별자치시":(350, 720), "경기도":(330, 810), "강원도":(480, 900),
                "충청북도":(400, 740), "충청남도":(280, 680), "경상북도":(580, 670), "경상남도":(500, 450),
                "전라북도":(300, 520), "전라남도":(290, 350), "제주특별자치도":(190, 100)}
    lst = member_service.Count_member()
    size = [i[1] * 10 for i in lst if i[0] in location.keys()]
    x = [location[i[0]][0] for i in lst if i[0] in location.keys()]
    y = [location[i[0]][1] for i in lst if i[0] in location.keys()]
    img_path = "static/graph/loc_plot1.png"
    img = plt.imread("./static/img/map.png")
    fig, ax = plt.subplots()
    ax.imshow(img, extent = [0, 800, 0, 1000])
    ax.axis('off')
    plt.scatter(x, y, s = size, c = 'r')
    fig.savefig(img_path)
    img_path1 = '/' + img_path

    loc = [i[0] for i in lst if i[0] in location.keys()]
    result = [i[1] for i in lst if i[0] in location.keys()]
    img_path = "static/graph/loc_plot2.png"
    fig, ax = plt.subplots()
    plt.pie(result, labels = loc, autopct="%.1f%%")
    fig.savefig(img_path)  # 그래프 이미지 파일로 저장
    img_path2 = '/' + img_path

    return render_template("/member/loc.html", img_path1 = img_path1, img_path2 = img_path2)