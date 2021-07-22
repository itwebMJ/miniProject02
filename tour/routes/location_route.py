from flask import Blueprint, render_template, request, redirect, session
import tour.models.location as loc

bp = Blueprint('location', __name__, url_prefix='/location')
areaService = loc.AreaService()


@bp.route('/')
def list(): #http://127.0.0.1:5000/location/
    areaList = areaService.areaBasedList(35)    #경북지역코드 35
    return render_template('location/location_index.html', areaList=areaList)

@bp.route('/get')
def get():
    areaList = areaService.areaBasedList(35)
    return render_template('location/detail.html', areaList=areaList)
