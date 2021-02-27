# -*-coding:utf-8-*- 
"""
通用文字识别，高精度版/普通版
created by boole @ 2021-02-27
"""

import os
import time
import requests
import base64

# request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"  # 普通版
request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"  # 高精版
access_token = ''

request_url = request_url + "?access_token=" + access_token
headers = {'content-type': 'application/x-www-form-urlencoded'}

file_dir = "./test_img/"
filelist =  os.listdir(file_dir)
for filename in filelist:
    time.sleep(0.5)
    if "_" in filename:
        continue
    filepath = os.path.join(file_dir, filename)
    # 二进制方式打开图片文件
    f = open(filepath, 'rb')
    img = base64.b64encode(f.read())
    params = {"image":img}

    response = requests.post(request_url, data=params, headers=headers)
    if response:
        ret = response.json()
        try:
            new_filename = ret["words_result"][0]["words"] + "_" + filename
            os.rename(filepath, os.path.join(file_dir, new_filename))
            print(filepath + ' --> ' + new_filename)
        except Exception as e:
        	print(filepath + ' --> ' + str(ret))
