from flask import Blueprint, render_template, request, redirect, session
import tour.models.location as loc
import tour.models.member as m
import tour.models.coronainfo as c_info

bp = Blueprint('location', __name__, url_prefix='/location')
areaService = loc.AreaService()
member_service = m.cMember_service()
coronainfo_service = c_info.CoronaService()

@bp.route('/area-code')
def area_code():
    areas = areaService.areaCode(17, 1)    #10개 데이터(numOfRows) 페이지 번호(pageNo)
    # 지역메뉴 밑의 이미지
    img_1 = areaService.detailImage(127291)
    img_2 = areaService.detailImage(128022)
    img_3 = areaService.detailImage(2638440)
    return render_template('location/area_menu.html', areas=areas, img_1=img_1, img_2=img_2, img_3=img_3)

@bp.route('/list')
def areaList():
    areaCode = request.args.get('areaCode', 0, int)
    print(areaCode)
    areaList = areaService.areaBasedList(areaCode, 30, 1)    #경북지역코드 35
    return render_template('location/area_list.html', areaList=areaList)

@bp.route('/list-detail')
def list_detail():
    contentid = request.args.get('contentid', 0, int)
    detailVo = areaService.detailCommon(contentid)  #img없는 detail
    for idx, i in enumerate(detailVo):
        detailVo[idx].overview = i.overview.replace("<br />", "\n")
        detailVo[idx].overview = i.overview.replace("<br>", "\n")
    print()
    img_1 = areaService.detailImage(contentid)      #img만
    return render_template('location/list_detail.html', detailVo=detailVo, img_1=img_1)

@bp.route('/search', methods=['POST'])
def search():
    keyword = request.form['keyword']
    searchList = areaService.searchKeyword(keyword, 30, 1)
    return render_template('location/area_list.html', areaList=searchList)

@bp.route("/interest")
def interest() :
    loc = request.args.get("loc", "", str)
    contentid = request.args.get("contentid", 0, int)
    loc_lst = loc.split()
    session["interest"] = loc_lst[0]
    member_service.Edit_member(loc_lst[0], session["id"])
    return redirect("/location/list-detail?contentid="+str(contentid))

@bp.route('/recommend')
def recommend():
    coronainfo = coronainfo_service.getCoronaGraph()
    #0번째는 검역
    areaList1 = areaService.searchKeyword(coronainfo[1].gubun, 5, 1)
    areaList2 = areaService.searchKeyword(coronainfo[2].gubun, 5, 1)
    areaList3 = areaService.searchKeyword(coronainfo[3].gubun, 5, 1)

    return render_template('location/rec_list.html', areaList1=areaList1,
                           areaList2=areaList2, areaList3=areaList3)


