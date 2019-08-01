import os
import numpy as np
import skimage.io as io
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
    RandomCrop,
    Resize
)

resolution = (256, 256)

def gen(path='data/train', batch=2):

    seed(42)
    images = []
     
    for file in os.listdir(f'{path}/left/'):
        images.append((f'{path}/left/{file}', f'{path}/depth/{file}', f'{path}/mask/{file}'))
        
    shuffle(images)
    #x = 0
    while True:
        output = []
        
        for _ in range(batch):
            img, depth, mask = choice(images)
            """
            save_img = img.split('/')[-1]
            save_depth = depth.split('/')[-1]
            copyfile(depth,f'{path}save/depth_4_mask/{x}_{save_depth}')
            copyfile(img,f'{path}save/left_4_mask/{x}_{save_img}')
            """
            img, depth, mask = io.imread(img), io.imread(depth), io.imread(mask)
            img, depth, mask = img[:,:,0:3], depth[:,:,0:3], mask[:,:,0:3]
            #print("before:")
            #print(np.unique(mask, axis=-2))
            aug1 = Compose([
                RandomCrop(height=resolution[0], width=resolution[1], p=1.0),
                VerticalFlip(p=0.5),
                RandomRotate90(p=0.5)],
                #OpticalDistortion(p=0.8, distort_limit=0.2, shift_limit=0.2)],
                additional_targets={
                    'depth': 'image',
                    'mask': 'image'
                })(image = img,
                depth = depth,
                mask = mask)
            aug2 = Compose([
                CLAHE(p=0.8),
                RandomBrightnessContrast(p=0.8),
                RandomGamma(p=0.8)])(image = aug1["image"])
            output.append((aug2["image"], aug1["depth"], aug1["mask"]))
            #x += 1

        yield output
"""
for imgs in gen():
    cv2.imshow('img0',imgs[0][0])
    cv2.imshow('img1',imgs[1][0])
    cv2.imshow('depth0',imgs[0][1])
    cv2.imshow('depth1',imgs[1][1])
    cv2.imshow('mask0',imgs[0][2])
    cv2.imshow('mask1',imgs[1][2])
    cv2.waitKey()
"""
def image_to_probs(img: np.ndarray) -> list:
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

def probs_to_image(imgs: list) -> np.ndarray:
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