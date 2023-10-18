#----------------------------------------------------#
#   对视频中的predict.py进行了修改，
#   将单张图片预测、摄像头检测和FPS测试功能
#   整合到了一个py文件中，通过指定mode进行模式的修改。
#----------------------------------------------------#
import time

import cv2
import numpy as np

from retinaface import Retinaface
from PIL import Image

from pathlib import Path
face_nn_path = Path(__file__).absolute().parent

def get_feature(image):
    pass

def recognize():
    image = Image.open(Path(__file__).parent.parent / 'image.jpg')
    image = image.rotate(270, expand=True)#.resize(image.size)
    # rotated_image.show()

    retinaface = Retinaface()
    result = retinaface.recognize_faces(image)
    return result

if __name__ == "__main__":
    names = recognize()
    exit()
    retinaface = Retinaface()
    #----------------------------------------------------------------------------------------------------------#
    #   mode用于指定测试的模式：
    #   'predict'表示单张图片预测，如果想对预测过程进行修改，如保存图片，截取对象等，可以先看下方详细的注释
    #   'video'表示视频检测，可调用摄像头或者视频进行检测，详情查看下方注释。
    #   'fps'表示测试fps，使用的图片是img里面的street.jpg，详情查看下方注释。
    #   'dir_predict'表示遍历文件夹进行检测并保存。默认遍历img文件夹，保存img_out文件夹，详情查看下方注释。
    #----------------------------------------------------------------------------------------------------------#
    mode = "predict"
    video_path      = 0
    video_save_path = ""
    video_fps       = 25.0
    #-------------------------------------------------------------------------#
    #   test_interval用于指定测量fps的时候，图片检测的次数
    #   理论上test_interval越大，fps越准确。
    #-------------------------------------------------------------------------#
    test_interval   = 100
    #-------------------------------------------------------------------------#
    #   dir_origin_path指定了用于检测的图片的文件夹路径
    #   dir_save_path指定了检测完图片的保存路径
    #   dir_origin_path和dir_save_path仅在mode='dir_predict'时有效
    #-------------------------------------------------------------------------#
    dir_origin_path = "img/"
    dir_save_path   = "img_out/"

    image = Image.open(Path(__file__).parent.parent / 'image.jpg')
    get_feature(image)
    exit()

    if mode == "predict":
        '''
        predict.py有几个注意点
        1、无法进行批量预测，如果想要批量预测，可以利用os.listdir()遍历文件夹，利用cv2.imread打开图片文件进行预测。
        2、如果想要保存，利用cv2.imwrite("img.jpg", r_image)即可保存。
        3、如果想要获得框的坐标，可以进入detect_image函数，读取(b[0], b[1]), (b[2], b[3])这四个值。
        4、如果想要截取下目标，可以利用获取到的(b[0], b[1]), (b[2], b[3])这四个值在原图上利用矩阵的方式进行截取。
        5、在更换facenet网络后一定要重新进行人脸编码，运行encoding.py。
        '''
        while True:
            img = input('Input image filename:')
            image = cv2.imread(img)
            if image is None:
                print('Open Error! Try again!')
                continue
            else:
                image   = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
                r_image = retinaface.detect_image(image)
                r_image = cv2.cvtColor(r_image,cv2.COLOR_RGB2BGR)
                cv2.imshow("after",r_image)
                cv2.waitKey(0)

    elif mode == "dir_predict":
        import os

        from tqdm import tqdm

        img_names = os.listdir(dir_origin_path)
        for img_name in tqdm(img_names):
            if img_name.lower().endswith(('.bmp', '.dib', '.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm', '.tif', '.tiff')):
                image_path  = os.path.join(dir_origin_path, img_name)
                image       = cv2.imread(image_path)
                image       = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
                r_image     = retinaface.detect_image(image)
                r_image     = cv2.cvtColor(r_image,cv2.COLOR_RGB2BGR)
                if not os.path.exists(dir_save_path):
                    os.makedirs(dir_save_path)
                cv2.imwrite(os.path.join(dir_save_path, img_name), r_image)
    else:
        raise AssertionError("Please specify the correct mode: 'predict', 'video', 'fps' or 'dir_predict'.")
