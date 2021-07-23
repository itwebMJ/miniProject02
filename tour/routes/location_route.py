from flask import Blueprint, render_template, request, redirect, session
import tour.models.location as loc

bp = Blueprint('location', __name__, url_prefix='/location')
areaService = loc.AreaService()


@bp.route('/area-code')
def area_code(): #http://127.0.0.1:5000/location/code
    areas = areaService.areaCode(17, 1)    #10개 데이터(numOfRows) 페이지 번호(pageNo)
    cart1_list = areaService.categoryCode_cart1()       # 대분류
    cart2_list = areaService.categoryCode_cart2(12)     # 중불류
    return render_template('location/area_code.html', areas=areas, cart1_list=cart1_list, cart2_list=cart2_list)

@bp.route('/list')
def areaList(): #http://127.0.0.1:5000/location/list
    areaCode = request.args.get('areaCode', 0, int)
    print(areaCode)
    areaList = areaService.areaBasedList(areaCode)    #경북지역코드 35
    return render_template('location/location_index.html', areaList=areaList)

@bp.route('/get')
def get():
    areaList = areaService.areaBasedList(35)
    return render_template('location/detail.html', areaList=areaList)
