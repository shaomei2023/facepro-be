import os, sys
from pathlib import Path
face_nn_path = Path(__file__).absolute().parent
sys.path.insert(0, str(face_nn_path))

from face_nn.retinaface import Retinaface

'''
在更换facenet网络后一定要重新进行人脸编码，运行encoding.py。
'''
retinaface = Retinaface(1)
dataset_path = face_nn_path/"face_nn/face_dataset"
list_dir = os.listdir(dataset_path)
image_paths = []
names = []
for name in list_dir:
    image_paths.append(dataset_path/name)
    names.append(name.split("_")[0])

retinaface.encode_face_dataset(image_paths,names)
