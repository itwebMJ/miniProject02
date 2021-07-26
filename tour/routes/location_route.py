from flask import Blueprint, render_template, request, redirect, session
import tour.models.location as loc

bp = Blueprint('location', __name__, url_prefix='/location')
areaService = loc.AreaService()


@bp.route('/area-code')
def area_code():
    areas = areaService.areaCode(17, 1)    #10개 데이터(numOfRows) 페이지 번호(pageNo)
    #cart1_list = areaService.categoryCode_cart1()       # 대분류
    #cart2_list = areaService.categoryCode_cart2(12)     # 중불류
    # 지역메뉴 밑의 이미지
    img_1 = areaService.detailImage(127291)
    img_2 = areaService.detailImage(128022)
    img_3 = areaService.detailImage(2638440)
    return render_template('location/area_menu.html', areas=areas, img_1=img_1, img_2=img_2, img_3=img_3)

@bp.route('/list')
def areaList():
    areaCode = request.args.get('areaCode', 0, int)
    print(areaCode)
    areaList = areaService.areaBasedList(areaCode, 10, 1)    #경북지역코드 35
    return render_template('location/area_list.html', areaList=areaList)

@bp.route('/list-detail')
def list_detail():
    contentid = request.args.get('contentid', 0, int)
    detailVo = areaService.detailCommon(contentid)  #img없는 detail
    print(detailVo)
    img_1 = areaService.detailImage(contentid)      #img만
    return render_template('location/list_detail.html', detailVo=detailVo, img_1=img_1)

@bp.route('/search', methods=['POST'])
def search():
    keyword = request.form['keyword']
    searchList = areaService.searchKeyword(keyword)
    return render_template('location/area_list.html', areaList=searchList)
