import numpy as np 
import os
import skimage.io as io
import skimage.transform as trans
from preprocess_png import gen, image_to_probs, probs_to_image
import re
import codecs, json 
import cv2

ground = [0,0,0]
trees = [0,255,0]
bush = [0,255,0]
towers = [0,0,255]
wires = [0,0,255]
copter = [255,255,255]
cars = [255,0,255]
buildings = [255,255,0]

COLOR_DICT = dict(ground = ground, trees = trees, bush = bush, towers = towers, wires = wires, copter = copter, cars = cars, buildings = buildings)


def adjustData(img, mask, channels):
    """
    Соответствует ли пиксель классу
    """
    img = img / 255  
    new_mask = np.zeros(mask[:, :, :, 0].shape + (len(channels),))
        
    for ch, color in enumerate(channels):
        new_mask[:, :, :, ch] = (mask == COLOR_DICT[color]).all(axis=-1)

    return (img, new_mask)

def trainGenerator(channels: list):
    """
    Генератор изображения для обучения
    Возвращает кортеж из элементов (batch_size, 255, 255, 3)
    """    
    train_generator = gen()
    for (img1, img2) in train_generator:
        
        img_0 = img1[0]
        img_1 = img2[0]
        mask_0 = img1[2]
        mask_1 = img2[2]
        img = np.array((img_0, img_1))
        mask = np.array((mask_0, mask_1))
        img, mask = adjustData(img, mask, channels)

        yield (img, mask)

def testGenerator(test_path: str) -> np.ndarray:
    """
    Генератор для predict.py
    Берет изображения из test_path, делит изображения на кусочки (1, 256, 256, 5)
    возвращает кусочки поочередно
    """
    files = os.listdir(test_path)
    files.sort(key = lambda x: int(re.search(r'\d+', x).group()))
    for file in files:
        img = io.imread(os.path.join(test_path, file))
        img = img / 255
        for img in image_to_probs(img):
            img = img[:,:,0:3]
            img = np.reshape(img, (1,)+img.shape)

            yield img

def color(item, channels):
    """
    Закрашивает пиксели в завесимости от класса и значения вероятности класса
    """
    rgb_matrix = np.zeros((len(channels),3))
    for ch, color in enumerate(channels):
        rgb_matrix[ch] = COLOR_DICT[color]
    img = np.zeros((item.shape[0],item.shape[1],3))
    img[:,:] = np.matmul(item[:,:],rgb_matrix)
    return img

def saveResult(save_path, output, channels, frame_number, cords) -> None:
    """
    Получает результаты предикта, собирает изображение из кусочков и сохраняет в 'save_path'
    """
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    arr = []
    for item in output:
        img = color(item, channels)
        arr.append(img)
        if len(arr)==15:
            img_save = probs_to_image(arr)
            img_save = img_save.astype(np.uint8)
            img_save = cv2.circle(img_save, (cords[1], cords[0]), 20, (255, 0, 0), 2)
            io.imsave(os.path.join(save_path, f"{frame_number}.png"), img_save)
            arr.clear()

def save_to_json(object, filepath):
    json.dump(object, codecs.open(filepath, 'w'), separators=(',',':'))

def read_from_json(filepath):
    data = codecs.open(filepath, 'r', encoding='utf-8').read()
    json_data = json.loads(data)
    return json_data
        
        