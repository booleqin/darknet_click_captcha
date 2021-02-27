# -*-coding:utf-8 -*-
"""
剪裁目标文件
"""
import time
import gc
import os
import random
import hashlib
import cv2
from PIL import Image

import sys
sys.path.append('/xxx/darknet/darknet-master')

from detect_base import get_detect_ret 

# 随机字符串
complex_str = "sagbjlagdjvwifqwasdvxjkwfadvnwfkegasaodqwgqg"


def detect_cut(img_dir, cut_dir):
    """
    识别定位框
    """
    filelist =  os.listdir(img_dir)
    for filename in filelist:
        img_path = os.path.join(img_dir, filename)
        ret = get_detect_ret(img_path.encode(encoding="utf-8"))
        img = cv2.imread(img_path)
        # img = Image.open(img_path)
        for i in ret:
            x_min, x_max = int(i[2][0] - i[2][2] / 2), int(i[2][0] + i[2][2] / 2)
            y_min, y_max = int(i[2][1] - i[2][3] / 2), int(i[2][1] + i[2][3] / 2)
            cut_img = img[y_min:y_max, x_min:x_max]
            # 生成随机加密串
            string_list = []
            for i in range(15):
                string_list.append(random.choice(complex_str))
            rstr = ''.join(string_list)
            hl = hashlib.md5()
            hl.update(rstr.encode(encoding='utf-8'))
            new_str = hl.hexdigest()
            cv2.imwrite(cut_dir + "/" + new_str + ".jpg", cut_img)
            # 内存释放
            del cut_img
            gc.collect()
        del img
        gc.collect()


if __name__ == '__main__':
    img_dir = "xxx"  # 需要裁剪的文件所在目录
    cut_dir = "xxx"  # 裁剪后存储的目录
    detect_cut(img_dir, cut_dir)



