# -*-coding:utf-8-*- 
"""
数据增强
created by boole @ 2021-02-27
"""

import re
import time
import os
import numpy as np
import cv2
import shutil
import hashlib

input_dir = "/xxx/cutting/mark_all"  # 已经标记好文件所在目录
obj_dir = "/xxx/classifier/train"  # 训练目录
obj_class = "/xxx/classifier/class.labels"  # labels存储目录


# 去除黑边的操作
crop_image = lambda img, x0, y0, w, h: img[y0:y0+h, x0:x0+w]

def rotate_image(img, angle, crop):
    """
    angle: 旋转的角度
    crop: 是否需要进行裁剪，布尔向量
    """
    w, h = img.shape[:2]
    angle %= 360
    # 计算仿射变换矩阵
    M_rotation = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1)
    # 得到旋转后的图像
    img_rotated = cv2.warpAffine(img, M_rotation, (w, h))

    if crop:
        angle_crop = angle % 180
        if angle > 90:
            angle_crop = 180 - angle_crop
        theta = angle_crop * np.pi / 180
        hw_ratio = float(h) / float(w)
        tan_theta = np.tan(theta)
        numerator = np.cos(theta) + np.sin(theta) * np.tan(theta)

        r = hw_ratio if h > w else 1 / hw_ratio
        denominator = r * tan_theta + 1
        crop_mult = numerator / denominator

        w_crop = int(crop_mult * w)
        h_crop = int(crop_mult * h)
        x0 = int((w - w_crop) / 2)
        y0 = int((h - h_crop) / 2)
        img_rotated = crop_image(img_rotated, x0, y0, w_crop, h_crop)
    return img_rotated


def gasuss_noise(image, mean=0, var=0.01):
    ''' 
        添加高斯噪声
        mean : 均值
        var : 方差
    '''
    image = np.array(image/255, dtype=float)
    noise = np.random.normal(mean, var ** 0.5, image.shape)
    out = image + noise
    if out.min() < 0:
        low_clip = -1.
    else:
        low_clip = 0.
    out = np.clip(out, low_clip, 1.0)
    out = np.uint8(out*255)
    #cv.imshow("gasuss", out)
    return out


kernel_emboss = np.array((
    [-2, -1, 0],
    [-1, 1, 1],
    [0, 1, 2]), dtype="float32")


filelist =  os.listdir(input_dir)
class_list = []
n = 0
for f_name in filelist:
    if f_name.split(".")[-1] not in ["jpg", "png"]:
        continue
    c = f_name.split("_")[0]
    if c == '.' and c == '.DS':
        continue
    n += 1
    if n % 500 == 0:
        print(n)
    
    source = input_dir + "/" + f_name
    target = obj_dir + "/" + f_name
    shutil.copy(source, target)
    
    ori_img = cv2.imread(source)
    # 灰度图
    obj_gray = cv2.cvtColor(ori_img, cv2.COLOR_RGB2GRAY)
    rstr = f_name.split("_")[1]
    hl = hashlib.md5()
    hl.update(rstr.encode(encoding='utf-8'))
    new_str = hl.hexdigest()
    cv2.imwrite(obj_dir + "/" + c + "_" + new_str + ".jpg", obj_gray)
    # 旋转15度
    image_rotated1 = rotate_image(ori_img, 15, False)
    rstr = new_str
    hl = hashlib.md5()
    hl.update(rstr.encode(encoding='utf-8'))
    new_str = hl.hexdigest()
    cv2.imwrite(obj_dir + "/" + c + "_" + new_str + ".jpg", image_rotated1)
    # 旋转-15度
    image_rotated2 = rotate_image(ori_img, 345, False)
    rstr = new_str
    hl = hashlib.md5()
    hl.update(rstr.encode(encoding='utf-8'))
    new_str = hl.hexdigest()
    cv2.imwrite(obj_dir + "/" + c + "_" + new_str + ".jpg", image_rotated2)
    # 高斯噪声
    image_gasuss = gasuss_noise(ori_img)
    rstr = new_str
    hl = hashlib.md5()
    hl.update(rstr.encode(encoding='utf-8'))
    new_str = hl.hexdigest()
    cv2.imwrite(obj_dir + "/" + c + "_" + new_str + ".jpg", image_gasuss)
    # emboss算子
    image_emboss = cv2.filter2D(ori_img, -1, kernel_emboss)
    rstr = new_str
    hl = hashlib.md5()
    hl.update(rstr.encode(encoding='utf-8'))
    new_str = hl.hexdigest()
    cv2.imwrite(obj_dir + "/" + c + "_" + new_str + ".jpg", image_emboss)
    
    if c not in class_list:
        class_list.append(c)
    # break


file_write_obj = open(obj_class, 'w') 
for var in class_list:
    if var == '.':  # 生成的时候会包含一个 . ，过滤
        continue
    file_write_obj.writelines(var) 
    file_write_obj.write('\n') 
file_write_obj.close()

