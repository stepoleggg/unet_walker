import numpy as np 
import os
import skimage.io as io
import skimage.transform as trans
from preprocess_png import gen, image_to_probs, probs_to_image

ground = [0,0,0]
trees = [0,255,0]
bush = [0,255,255]
towers = [0,0,255]
wires = [0,0,255]
copter = [255,255,255]
cars = [255,0,255]
buildings = [255,255,0]

COLOR_DICT = dict(ground = ground, trees = trees, bush = bush, towers = towers, wires = wires, copter = copter, cars = cars, buildings = buildings)


def adjustData(img, mask, flag_multi_class, channels):
    """
    Соответствует ли пиксель классу
    """
    if(flag_multi_class):

        img = img / 255  
        new_mask = np.zeros(mask[:, :, :, 0].shape + (len(channels),))
        
        for ch, color in enumerate(channels):
            new_mask[:, :, :, ch] = (mask == COLOR_DICT[color]).all(axis=-1)

        return (img, new_mask)



def trainGenerator(channels: list, flag_multi_class=True):
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
        img, mask = adjustData(img, mask, flag_multi_class, channels)

        yield (img, mask)



def testGenerator(test_path: str) -> np.ndarray:
    """
    Генератор для predict.py
    Берет изображения из test_path, делит изображения на кусочки (1, 256, 256, 5)
    возвращает кусочки поочередно
    """
    for file in os.listdir(test_path):
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
    img = np.zeros(item[:,:,0].shape + (3,), dtype = np.uint8)
    for y in range(len(img)):
        for x in range(len(img[y])):
            m_ch_v = np.max(item[y][x])
            m_ch_i = np.where(item[y][x] == m_ch_v)
            m_ch_i = m_ch_i[0][0]
            
            img[y][x][0] = int(COLOR_DICT[channels[m_ch_i]][0]*m_ch_v)
            img[y][x][1] = int(COLOR_DICT[channels[m_ch_i]][1]*m_ch_v)
            img[y][x][2] = int(COLOR_DICT[channels[m_ch_i]][2]*m_ch_v)
            """
            if m_ch_v > 0.5:
                img[y][x][0] = int(COLOR_DICT[channels[m_ch_i]][0])
                img[y][x][1] = int(COLOR_DICT[channels[m_ch_i]][1])
                img[y][x][2] = int(COLOR_DICT[channels[m_ch_i]][2])
            else:
                img[y][x][0] = 255
                img[y][x][1] = 255
                img[y][x][2] = 255
            """
    return img

def saveResult(save_path, npyfile, channels):
    arr = []
    k = 0
    for _, item in enumerate(npyfile):

        img = color(item, channels)
        arr.append(img)
        if len(arr)==15:
            img_save = probs_to_image(arr)
            img_save = img_save.astype(np.uint8)
            k+=1
            io.imsave(os.path.join(save_path,"%d_predict.png"%k), img_save)
            arr = []
        
        