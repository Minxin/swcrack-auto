
# -*- coding: utf-8 -*-
# @Time : 2022/05/24
# @Author : fancy
# @Instructions : 速蛙云（https://i.sw12.icu/hDR1）机场限时优惠抢购脚步，功能包括爆破滑块验证登录、定时抢购。滑块多次失败后可能报错退出，但不会限制登录，可以重复尝试。

import schedule
import time
import requests
import json
import threading

import base64
import numpy as np
import cv2 as cv



name="youremail"
password="yourpasswd"



buy_url = "https://m.ok8.icu/api_mweb/shop/buy"
captcha_url="https://m.ok8.icu/api_mweb/captcha"
check_url="https://m.ok8.icu/api_mweb/captcha/check"
login_url="https://m.ok8.icu/api_mweb/login"
list_url="https://m.ok8.icu/api_mweb/shop/list"


# def hk(img):
#     # img = np.array(img)  # 转化为numpy
#     # img = cv.resize(img, (150, 300))  # 用cv2resize
#     # img = img[:, :, (2, 1, 0)]  # BGR图像转RGB
#     print(img)
#     print(img.shape)
#     img1 = img.copy()
#     # 将通道值小于150的转变为黑色
#     for h in range(img.shape[0]):
#         for w in range(img.shape[1]):
#             if img[h, w, 0] < 150 and img[h, w, 1] < 150 and img[h, w, 2] < 150:
#                 for c in range(3):
#                     img[h, w, c] = 0
#             else:
#                 for c in range(3):
#                     img[h, w, c] = 255
#     canny_img = cv.Canny(img, 50, 100)  # 边缘检测
#     counts, _ = cv.findContours(canny_img, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)  # 轮廓检测
#     for c in counts:
#         x, y, w, h = cv.boundingRect(c)
#         #  去除较小先验框
#         if w < 20:
#             continue
#         if h < 20:
#             continue
#         cv.rectangle(img1, (x, y), (x + w, y + h), (0, 0, 255), 2)
#         print(f"左上点的坐标为：{x, y}，右下点的坐标为{x + w, y + h}")
#     return img1











#------------------------------The slider check----------------------------
def getx(contours):
    for i, contour in enumerate(contours):  # 所有轮廓
        if 1600 < cv.contourArea(contour) <= 2500 and 160 < cv.arcLength(contour, True) < 220:
            x, y, w, h = cv.boundingRect(contour)  # 外接矩形
            print(x, y, w, h)
            #cv.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
            return x/(300-45)



captcha_head={
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "authorizationmweb": "faster",
    "cookie": "_ga=GA1.1.735359788.1653383307; _gcl_au=1.1.1811677344.1653383307; _ga_TVRF6RYBHW=GS1.1.1653383298.1.1.1653383307.0",
    "referer": "https://m.ok8.icu/m/login",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36 Edg/86.0.622.69"
    }

def check():
    captcha_response=requests.get(captcha_url,headers=captcha_head)
    captcha_json=json.loads(captcha_response.content.decode('utf-8'))
    data_json=captcha_json["data"]

    token=data_json["token"]
    bg_img=data_json["bg"]
    puzz_img=data_json["puzz"]
    bgimg=bg_img.split(',')[-1]


    puzzimg=puzz_img.split(',')[-1]
    puzzimg=base64.b64decode(puzzimg)
    nparray_puzz_img=np.frombuffer(puzzimg,dtype=np.uint8)
    puzz_cvimg = cv.imdecode(nparray_puzz_img,-1)
    cv.imwrite("puzz.png",puzz_cvimg)
    print(puzz_cvimg.shape)
    up_border=0
    for i in range(puzz_cvimg.shape[0]):
        pix=puzz_cvimg[i][30]
        pix_value=pix[0]+pix[1]+pix[2]+pix[3]
        if pix_value>0:
            up_border=i
    print("upper_border:",up_border,"  lower_border:",up_border+50)
    puzz_cvimg=puzz_cvimg[up_border-50:up_border+5,0:49]
    blurred = cv.GaussianBlur(puzz_cvimg, (7, 7), 0)
    canny = cv.Canny(blurred, 250, 300)
    cv.imwrite("puzz_canny.png",canny) 
    puzz_contours, puzz_hierarchy = cv.findContours(canny, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE)


    #image = cv.imread(image_path)
    b64decode_img=base64.b64decode(bgimg)
    nparray_img=np.frombuffer(b64decode_img,dtype=np.uint8)
    image = cv.imdecode(nparray_img,-1)
    # cv.imshow("xxx",hk(image))
    # cv.waitKey(5000)

    # B,G,R=cv.split(image)
    # hsv_img=cv.cvtColor(image,cv.COLOR_BGR2HSV)
    # H,S,V=cv.split(hsv_img)
    # ret1, thres= cv.threshold(V, 200, 255, cv.THRESH_BINARY_INV)
    # cv.imshow('thres', thres)
    # cv.waitKey(5000)
    cv.imwrite("bg.png",image)
    print(image.shape)
    image=image[up_border-50:up_border+5,0:299]
    print(image.shape)
    blurred = cv.GaussianBlur(image, (7, 7), 0)
    canny = cv.Canny(blurred, 80, 100)

    cv.imwrite("canny.png",canny) 

    bg_contours, bg_hierarchy = cv.findContours(canny, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE)
    offset=getx(bg_contours,)
    return offset,token

# print(puzz_contours)
# print("------------")
# print(bg_contours)
# hausdorff_sd = cv.createHausdorffDistanceExtractor()
# d1 = hausdorff_sd.computeDistance(bg_contours, puzz_contours)
# print(d1)



# for i, contour in enumerate(contours):  # 所有轮廓
#     x, y, w, h = cv.boundingRect(contour)  # 外接矩形
#     if 45<w<52 and 45<h<52 or True:
#         temp=image.copy()
#         cv.rectangle(temp, (x, y), (x + w, y + h), (0, 0, 255), 2)
#         print(cv.contourArea(contour),cv.arcLength(contour, True))
#         #cv.imshow('image', temp)
#         cv.imwrite("temp"+str(x)+"_"+str(y)+"_"+str(w)+"_"+str(h)+".png",temp) 
# 



n=None
token=None
while n==None:
    n,token=check()


check_data={
    "email":name,
    "n":n,
    "passwd":password,
    "token":token
}
print(check_data)

head={
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "content-type": "application/json",
    "cookie": "_ga=GA1.1.735359788.1653383307; _gcl_au=1.1.1811677344.1653383307; _ga_TVRF6RYBHW=GS1.1.1653383298.1.1.1653383307.0",
    "origin": "https://m.ok8.icuu",
    "referer": "https://m.ok8.icu/m/check",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36 Edg/86.0.622.69"
}
check_response=requests.post(check_url,json=check_data,headers=head)
check_result=json.loads(check_response.content.decode('utf-8'))
print(check_result)
if(check_result["code"]!=100):
    print("fail")
else:
    token=check_result["data"]["token"]
    print(token)





#------------------------------login----------------------------
login_data={
    "email":name,
    "passwd":password,
    "token":token
}

login_head={
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "content-type": "application/json",
    "cookie": "_ga=GA1.1.735359788.1653383307; _gcl_au=1.1.1811677344.1653383307; _ga_TVRF6RYBHW=GS1.1.1653383298.1.1.1653383307.0",
    "origin": "https://m.ok8.icu",
    "referer": "https://m.ok8.icu/m/login",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36 Edg/86.0.622.69"
}

login_response=requests.post(login_url,json=login_data,headers=login_head)
login_result=json.loads(login_response.content.decode('utf-8'))
print(login_result)
if login_result["code"]==100:
    print("login success!")
else:
    print("login fail!")
print(login_response.headers)
authorizationmweb=login_response.headers["mweb-auth-token"]
Cookie=login_response.headers["Set-Cookie"]

buy_headers={
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "authorizationmweb": authorizationmweb,
    "content-type": "application/json",
    "cookie": Cookie,
    "origin": "https://m.ok8.icu",
    "referer": "https://m.ok8.icu/m/shop",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36 Edg/86.0.622.69"
}

list_response=requests.get(list_url,headers=buy_headers)
list_json=json.loads(list_response.content.decode('utf-8'))
id_to_buy=0

if list_json["code"]==100:
    goods=list_json["data"]
    mygoods={}
    for good in goods:
        print(good["id"],good["name"])
        mygoods[good["id"]]=good["name"]
    print(mygoods)
    id=input("choose which you buy?\n")
    print("you choose this ",mygoods[int(id)])
    id_to_buy=int(id)
    

#------------------------------time task for buying----------------------------
data={"coupon": "限时折扣", "id": id_to_buy, "upgrade":False}
def swtest():
    while True:
        coupon_response=requests.put(buy_url, json=data, headers=buy_headers)
        print(coupon_response.content)
        coupon_json=json.loads(coupon_response.content.decode('utf-8'))
        message=coupon_json["message"]
        print(message)


def run_threaded(job_func):
     job_thread = threading.Thread(target=job_func)
     job_thread.start()

buytime=input("set the time to buy (format is 12:23:34):\n")
schedule.every().day.at(buytime).do(run_threaded,swtest)
schedule.every().day.at(buytime).do(run_threaded,swtest)
schedule.every().day.at(buytime).do(run_threaded,swtest)
schedule.every().day.at(buytime).do(run_threaded,swtest)
while True:
    schedule.run_pending()   # 运行所有可以运行的任务
    time.sleep(1)
