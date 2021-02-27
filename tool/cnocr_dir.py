# -*-coding:utf-8-*- 
"""
基于cnocr开源库的识别
created by boole @ 2021-02-27
"""

import os
import time
import requests
import base64
from cnocr import CnOcr
ocr = CnOcr() 

# 二进制方式打开图片文件
file_dir = "./test_img/"
filelist =  os.listdir(file_dir)
for filename in filelist:
    if "_" in filename:
        continue
    filepath = os.path.join(file_dir, filename)
    ret = ocr.ocr(filepath)

    try:
        new_filename = ret[0][0] + "_" + filename
        os.rename(filepath, os.path.join(file_dir, new_filename))
        print(filepath + ' --> ' + new_filename)
    except Exception as e:
        print(filepath + ' --> ' + str(ret))
