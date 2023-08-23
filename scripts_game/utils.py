'''
tep nay dung de load image
'''

import pygame as pg
import os

CONST_IMG_PATH = 'data/images/'

def load_image(path):
    img = pg.image.load(CONST_IMG_PATH + path).convert() #convert giup hieu qua hon de ket xuat hình anh len pygame
    img.set_colorkey((0, 0, 0)) # se color co mau rgb cung ve trong suot
    return img

def load_images(path):
    # ung dung load cac hinh anh lap lai nhieu nhu gach da trong map
    images = []
    for img_name in os.listdir(CONST_IMG_PATH + path):
        images.append(load_image(path + '/' + img_name))
    return  images
