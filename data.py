from __future__ import print_function
from keras.preprocessing.image import ImageDataGenerator
import numpy as np 
import os
import glob
import skimage.io as io
import skimage.transform as trans
from scipy import ndimage, misc
from preprocess_png import gen, image_to_probs, probs_to_image
import cv2

ground = [0,0,0]
trees = [0,255,0]
bush = [0,255,255]
towers = [0,0,255]
wires = [0,0,255]
copter = [255,255,255]
cars = [255,0,255]
buildings = [255,255,0]

COLOR_DICT = dict(ground = ground, trees = trees, bush = bush, towers = towers, wires = wires, copter = copter, cars = cars, buildings = buildings)


def adjustData(img,mask,flag_multi_class,channels):
    if(flag_multi_class):
        img = img / 255
        new_mask = np.zeros(mask[:,:,:,0].shape + (len(channels),))
        #print(new_mask.shape)
        ch = 0
        for channel in channels:
            for b in range(len(new_mask)):
                for y in range(len(new_mask[b])):
                    for x in range(len(new_mask[b][y])):
                        new_mask[b][y][x][ch] = 1 if mask[b][y][x][0] == COLOR_DICT[channel][0] and mask[b][y][x][1] == COLOR_DICT[channel][1] and mask[b][y][x][2] == COLOR_DICT[channel][2] else 0
            ch += 1
        mask = new_mask
        #print(mask.shape)
        #print(np.amax(mask), np.amin(mask))
    elif(np.max(img) > 1):
        img = img / 255
        mask = mask /255
        mask[mask > 0.5] = 1
        mask[mask <= 0.5] = 0
    return (img,mask)



def trainGenerator(batch_size,train_path,image_folder,depth_folder,mask_folder,channels,aug_dict,image_color_mode = "rgb",
                    mask_color_mode = "rgb",image_save_prefix  = "image",mask_save_prefix  = "mask",
                    flag_multi_class = True,save_to_dir = None,target_size = (256,256),seed = 1):
        
    train_generator = gen()
    for (img1, img2) in train_generator:
        
        img_0 = img1[0]
        img_1 = img2[0]
        mask_0 = img1[2]
        mask_1 = img2[2]
        #print("after:")
        #print(np.unique(mask_0, axis=0))
        img = np.array((img_0, img_1))
        mask = np.array((mask_0, mask_1))
        img,mask = adjustData(img,mask,flag_multi_class,channels)
        yield (img,mask)



def testGenerator(test_path,save_path,num_image = 20,target_size = (256,256),flag_multi_class = True):
    i = 0
    for file in os.listdir(test_path):
        img = io.imread(os.path.join(test_path,file))
        img = img / 255
        for img in image_to_probs(img):
            i+=1
            img = trans.resize(img,target_size)
            #io.imsave(os.path.join(save_path,"%d_test.png"%i),img)
            img = img[:,:,0:3]
            img = np.reshape(img,(1,)+img.shape)

            yield img

def color(item, channels):
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

def saveResult(save_path,npyfile,channels):
    arr = []
    k = 0
    for i,item in enumerate(npyfile):
        #print(item)
        img = color(item, channels)
        arr.append(img)
        if len(arr)==15:
            img_save = probs_to_image(arr)
            img_save = img_save.astype(np.uint8)
            k+=1
            io.imsave(os.path.join(save_path,"%d_predict.png"%k),img_save)
            arr = []
        
        