from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from sqlalchemy import func
from app_.models.quiz_model import *
from app_.models.users_model import *
from app_.models.quiz_model import *
from app_.models.users_model import *

import requests
from bs4 import BeautifulSoup as bs

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/', methods=['GET', 'POST'])
@login_required
def index():
    data = {}
    data['title'] = 'Dashboard'
    score = Score.query\
        .join(User, Score.user_id == User.id)\
        .join(Subject, Score.subject_id == Subject.id)\
        .filter(User.user_role == 2)\
        .add_columns(Score.id, User.name, Subject.subject, Score.score)

    data['score'] = score
    data['total_user'] = len(User.query.all())
    data['total_question'] = len(Question.query.all())
    data['total_subject'] = len(Subject.query.all())

    url = "https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-Indonesia.xml"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get(url, headers=headers)
    r = response.text
    root = bs(r,"xml")
    n=4

    area = 'DKI Jakarta'  
    if request.method == 'POST':
        area = request.form.get('area')

    weather = root.find(domain=area).find(id="weather").find_all(type='hourly')
    arr_weather = []
    for i in weather:
        arr_weather.append(i.value.text)

    final_weather = [arr_weather[i * n:(i + 1) * n] for i in range((len(arr_weather) + n - 1) // n )]  

    temp = root.find(domain=area).find(id="t").find_all(type='hourly')
    arr_temp = []
    for i in temp:
        arr_temp.append(i.value.text)

    final_temp = [arr_temp[i * n:(i + 1) * n] for i in range((len(arr_temp) + n - 1) // n )]  

    wd = root.find(domain=area).find(id="wd").find_all(type='hourly')
    arr_wd = []
    for i in wd:
        arr_wd.append(i.value.text)

    final_wd = [arr_wd[i * n:(i + 1) * n] for i in range((len(arr_wd) + n - 1) // n )]  

    ws = root.find(domain=area).find(id="ws").find_all(type='hourly')
    arr_ws = []
    for i in ws:
        arr_ws.append(i.find(unit="MPH").text)

    final_ws = [arr_ws[i * n:(i + 1) * n] for i in range((len(arr_ws  ) + n - 1) // n )]  

    hum = root.find(domain=area).find(id="hu").find_all(type='hourly')
    arr_hum = []
    for i in hum:
        arr_hum.append(i.value.text)

    final_hum = [arr_hum[i * n:(i + 1) * n] for i in range((len(arr_hum) + n - 1) // n )]  

    hum_max = root.find(domain=area).find(id="humax").find_all(type='daily')
    final_hum_max = []
    for i in hum_max:
        final_hum_max.append(i.value.text)

    hum_min = root.find(domain=area).find(id="humin").find_all(type='daily')
    final_hum_min = []
    for i in hum_min:
        final_hum_min.append(i.value.text)

    tmax = root.find(domain=area).find(id="tmax").find_all(type='daily')
    final_tmax = []
    for i in tmax:
        final_tmax.append(i.find(unit="C").text)

    tmin = root.find(domain=area).find(id="tmin").find_all(type='daily')
    final_tmin = []
    for i in tmin:
        final_tmin.append(i.find(unit="C").text)

    forcast = {
        'title': area,
        'weather': final_weather,
        'temp': final_temp,
        'temp_max': final_tmax,
        'temp_min': final_tmin,
        'wind_dir': final_wd,
        'wind_sp': final_ws,
        'hum': final_hum,
        'hum_max': final_hum_max,
        'hum_min': final_hum_min,
        'headtime': {0: 'Yesterday', 1:'Today', 2:'Tomorrow'},
        'clock': {0: '00:00', 1:'06:00', 2:'12:00', 3:'18:00'},
        'area': ['Aceh', 'Bali', 'Banten', 'Bengkulu', 'DI Yogyakarta', 'DKI Jakarta', 'Gorontalo', 'Jambi', 'Jawa Barat', 'Jawa Tengah', 'Jawa Timur', 'Kalimantan Barat', 'Kalimantan Selatan', 'Kalimantan Tengah', 'Kalimantan Timur', 'Kalimantan Utara', 'Kep. Bangka Belitung', 'Kep. Riau', 'Lampung', 'Maluku', 'Maluku Utara', 'Nusa Tenggara Barat', 'Nusa Tenggara Timur', 'Papua', 'Papua Barat', 'Riau', 'Sulawesi Barat', 'Sulawesi Selatan', 'Sulawesi Tenggara', 'Sulawesi Utara', 'Sumatera Barat', 'Sumatera Selatan', 'Sumatera Utara', ]
    }

    return render_template('home/main.html', user=current_user, forcast=forcast, data=data)