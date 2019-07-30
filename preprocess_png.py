import os
import numpy as np
import cv2
from shutil import copyfile
from random import choice, shuffle, seed
from albumentations import (
    HorizontalFlip,
    VerticalFlip,
    CenterCrop,
    Crop,
    Compose,
    Transpose,
    RandomRotate90,
    ElasticTransform,
    GridDistortion,
    OpticalDistortion,
    RandomSizedCrop,
    OneOf,
    CLAHE,
    RandomBrightnessContrast,
    RandomGamma,
    RandomCrop
)

resolution = (256, 256)

def gen(path='data/train/', batch=2):
    seed(42)
    images = []
    for directory in os.listdir(path):
        d = f'{path}{directory}' 
        for file in os.listdir(f'{d}/left/'):
            images.append((f'{d}/left/{file}', f'{d}/depth/{file}'))
    shuffle(images)
    #x = 0
    while True:
        output = []
        
        for _ in range(batch):
            img, depth = choice(images)
            """
            save_img = img.split('/')[-1]
            save_depth = depth.split('/')[-1]
            copyfile(depth,f'{path}save/depth_4_mask/{x}_{save_depth}')
            copyfile(img,f'{path}save/left_4_mask/{x}_{save_img}')
            """
            img, depth = cv2.imread(img), cv2.imread(depth)
            aug1 = Compose([
                RandomCrop(height=resolution[0], width=resolution[1], p=1.0),
                VerticalFlip(p=0.5),
                RandomRotate90(p=0.5),
                OpticalDistortion(p=0.8, distort_limit=0.2, shift_limit=0.2)],
                additional_targets={
                    'depth': 'image'
                })(image = img,
                depth = depth)
            aug2 = Compose([
                CLAHE(p=0.8),
                RandomBrightnessContrast(p=0.8),
                RandomGamma(p=0.8)])(image = aug1["image"])
            output.append((aug2["image"], aug1["depth"]))
            #x += 1

        yield output
"""
for imgs in gen():
    cv2.imshow('img0',imgs[0][0])
    cv2.imshow('img1',imgs[1][0])
    cv2.imshow('depth0',imgs[0][1])
    cv2.imshow('depth1',imgs[1][1])
    cv2.waitKey()
"""
def image_to_probs(img):
    """
    На вход подается изображение (720,1280,3), оно делиться на равные прямоугольники (256,256,3)
    На выходе list прямоугольников
    Проход по изображению идет слева на право
    """
    out = []

    for i in range(0,3):
        for j in range(0,5):
            if i==2:
                new_image = img[i*256-48:(i+1)*256-48,j*256:(j+1)*256,:] # сдвиг, чтобы сохранить размер (720,1280,3) при сборке
            else:
                new_image = img[i*256:(i+1)*256,j*256:(j+1)*256,:]
            out.append(new_image)

    return out

def probs_to_image(imgs):
    """
    Собирает изображение из прямоугольников (256,256,3), на вход подается list прямоугольников
    Проход идет слева на право
    """
    new_image = np.zeros((720, 1280, 3,))
    k = 0
    for i in range(0,3):
        for j in range(0,5):
            img = imgs[k]
            if i==2:
                new_image[i*256-48:(i+1)*256-48,j*256:(j+1)*256,:] = img[:,:,:]
            else:
                new_image[i*256:(i+1)*256,j*256:(j+1)*256,:] = img[:,:,:]
            k+=1
            
    return new_image