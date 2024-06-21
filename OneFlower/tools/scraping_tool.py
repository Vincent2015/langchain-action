import json
import requests
import time
def scrape_weibo(url :str):
    headers = {
        "User-Agent": "Mozilla/5.0(Windows NT 10.0;Win64;X64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/89.0.4389.82.Safari/537.36",
        "Referer":"https://weibo.com"
    }
    cookies = {
        "cookie":'''XSRF-TOKEN=p-CHHfxT8fCLziogln0MXKAs; SUB=_2A25Ld9ZjDeRhGedG7FMT8yjIzzmIHXVoDVerrDV8PUNbmtANLU2jkW9NUQBchQcxoYrmBkHi7MBbzI_00TyU10Dy; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W53l7xNJgzXXvsj83vvCEwZ5NHD95Qp1hMpeoecShBfWs4Dqcj.i--Ri-zciKnfi--fiK.0i-2fi--Ri-zNi-zfi--Ri-2piKyh; ALF=02_1721447219; WBPSESS=UwBG5ezGjEkdxi7Pc_bkLjt8HSdzD15h_qlxvEuXeObY1d8s01FunwNNmNF1r_Iu_gpN3dZnNZPfhkMuxhhwjliLnE1Jlk4SPGbL0YwYF5aOv-h_su7tKhIqO6W9URK2cA_ClxgzZlgaiWnKeclikg=='''
    }

    response = requests.get(url,headers=headers,cookies=cookies)
    time.sleep(3)
    return response.text
def get_data(id):
    url ="https://weibo.com/ajax/profile/detail?uid={}".format(id)
    html = scrape_weibo(url)
    response = json.loads(html)

    return response