# -*-coding:utf-8-*- 
"""
api flask
created by boole @ 2021-02-27
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import os
import re
from logging_conf import logger
from time import time
from json import loads
from json import dumps
from ConfigParser import SafeConfigParser
from flask import Flask
from flask import request
import numpy as np
import cv2

service_dir = os.path.abspath(os.path.join(os.getcwd(), "./conf/service.conf"))
cp = SafeConfigParser()
cp.read(service_dir)
plat = cp.get("ServicePlat", "plat")
host = cp.get(plat, "host")
port = cp.get(plat, "port")

service_root = os.path.abspath(os.getcwd())
darknet_path = os.path.join(service_root, "darknet/darknet-master")
sys.path.append(darknet_path)

from detect_base import get_detect_ret as base_func
from detect_obj import get_detect_ret as obj_func
from classifier_pre import get_classify_ret


app = Flask(__name__)

# post
@app.route('/captcha/distinguish', methods=['POST'])
def distinguish_func():
    """
    detecting text position and content
    """
    # 格式检查
    start_time = time()
    result = {}
    result["code"] = 1
    if request.headers['Content-Type'] != 'application/json':
        msg = "request is not json"
        result["ret"] = msg
        logger.error("request is not json")
        return dumps(result)
    try:
        ret = dumps(request.json)
        dat = loads(ret)
        model = dat["model"]
        basefile = dat["basefile"]
        objfile = dat["objfile"]
    except Exception as e:
        msg = "The request is not legal"
        result["ret"] = msg
        logger.error(e)
        return dumps(result)
    
    # 计算
    if model == "classifier":
        try:
            base_ret = base_func(basefile.encode("utf-8"))
            obj_ret = obj_func(objfile.encode("utf-8"))
            img_base = cv2.imread(basefile)
            img_obj = cv2.imread(objfile)

            # 识别base图片
            cut_img_base = {}
            n = 0
            for i in base_ret:
                n += 1
                name = i[0]
                acc = i[1]
                x_min, x_max = int(i[2][0] - i[2][2] / 2), int(i[2][0] + i[2][2] / 2)
                y_min, y_max = int(i[2][1] - i[2][3] / 2), int(i[2][1] + i[2][3] / 2)
                cut_img = img_base[y_min:y_max, x_min:x_max]
                # 保存cut_img
                temp_file = service_root + "/cut_img/base_" + str(n) + ".jpg"
                cv2.imwrite(temp_file, cut_img)
                class_ret = get_classify_ret(temp_file.encode("utf-8"))
                cut_img_base[x_min] = class_ret[0][0]
            # 识别obj图片
            cut_img_obj = {}
            n = 0
            for i in obj_ret:
                n += 1
                x_min, x_max = int(i[2][0] - i[2][2] / 2), int(i[2][0] + i[2][2] / 2)
                y_min, y_max = int(i[2][1] - i[2][3] / 2), int(i[2][1] + i[2][3] / 2)
                cut_img = img_obj[y_min:y_max, x_min:x_max]
                # 保存cut_img
                temp_file = service_root + "/cut_img/obj_" + str(n) + ".jpg"
                cv2.imwrite(temp_file, cut_img)
                class_ret = get_classify_ret(temp_file.encode("utf-8"))
                cut_img_obj[class_ret[0][0]] = i[2]
            
            sorted_key = sorted(cut_img_base.keys())
            cut_img_base_tuple = [(sorted_key.index(k) + 1, cut_img_obj[cut_img_base[k]] if cut_img_base[k] in cut_img_obj else (50, 50, 50, 50)) 
                        for k in sorted(cut_img_base.keys())]
            result["code"] = 0
            result["ret"] = cut_img_base_tuple
            time_cost = time() - start_time
            log_dic = {"model": model, "basefile": basefile, "objfile": objfile, "ret": cut_img_base_tuple, "timecost": time_cost}
            logger.info(log_dic)
            return dumps(result)
        except Exception as e:
            msg = "classifier calculate error"
            result["ret"] = msg
            log_dic = {"model": model, "basefile": basefile, "objfile": objfile, "ret": msg}
            logger.error(log_dic)
            return dumps(result)
    elif model == "resemblance":
        msg = "Look forward to it"
        result["code"] = 0
        result["ret"] = msg
        return dumps(result)
    else:
        msg = "model type is error"
        result["ret"] = msg
        return dumps(result)


if __name__ == '__main__':
    """
    example
    curl -H "Content-type: application/json" -X POST http://host:port/captcha/distinguish -d '{"model": "classifier", "basefile": "", "objfile": ""}'
    """
    app.run(host=host, port=int(port), debug=True)
