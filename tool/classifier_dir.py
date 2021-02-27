# -*-coding:utf-8-*- 
"""
使用训练好的模型迭代标记
created by boole @ 2021-02-27
"""
import os
import time
import requests
import base64

# 这里需要把tool中的classifier_pre.py、detect_obj.py、detect_base.py 放到./darknet/darknet-master目录下
import sys
sys.path.append('/xxx/darknet/darknet-master')
from classifier_pre import get_classify_ret 
'''
# file
filepath = "./test_img/9e4b3b3e04f2cc6d131f658443c7d9fa.jpg"
ret = get_classify_ret(filepath.encode("utf-8"))
print(ret)
'''
file_dir = "./test_img/"
filelist =  os.listdir(file_dir)
for filename in filelist:
    if "_" in filename:
        continue
    filepath = os.path.join(file_dir, filename)
    try:
        ret = get_classify_ret(filepath.encode("utf-8"))
        new_filename = ret[0][0] + "_" + filename
        os.rename(filepath, os.path.join(file_dir, new_filename))
        print(filepath + ' --> ' + new_filename)
    except Exception as e:
        print(filepath + ' --> ' + str(ret))
