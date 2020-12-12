import time
import cv2
from random import randrange
from math import sqrt


def printTree(tree, img, color):
    for node in tree:
        for kid in node.kids:
            cv2.line(img, (node.x, node.y), (kid.x, kid.y), color, 1)


def dist(x1, y1, x2, y2):
    # return sqrt((x1 - x2)**2 + (y1 - y2)**2)
    return abs(x1 - x2) + abs(y1 - y2)


def drawPath(tree1, tree2):
    tree1.meetParent()
    tree2.meetParent()


def nearest(xsamp, ysamp, tree):
    d = [dist(xsamp, ysamp, n.x, n.y) for n in tree]
    near = d.index(min(d))
    nearNode = tree[near]
    return nearNode


def clear_(x, y, img):
    Size = 10
    xsize = Size
    ysize = Size
    if 0 < (x + xsize) and x + xsize < img.shape[1] - 1 and 0 < (y + ysize) and y + ysize < img.shape[0] - 1:
        if img[ro(y + ysize)][ro(x + xsize)][0] > 240 and img[ro(y + ysize)][ro(x + xsize)][1] > 240 and img[ro(y + ysize)][ro(x + xsize)][2] > 240:
            return False
    xsize = -Size
    ysize = Size
    if 0 < (x + xsize) and x + xsize < img.shape[1] - 1 and 0 < (y + ysize) and y + ysize < img.shape[0] - 1:
        if img[ro(y + ysize)][ro(x + xsize)][0] > 240 and img[ro(y + ysize)][ro(x + xsize)][1] > 240 and img[ro(y + ysize)][ro(x + xsize)][2] > 240:
            return False
    xsize = Size
    ysize = -Size
    if 0 < (x + xsize) and x + xsize < img.shape[1] - 1 and 0 < (y + ysize) and y + ysize < img.shape[0] - 1:
        if img[ro(y + ysize)][ro(x + xsize)][0] > 240 and img[ro(y + ysize)][ro(x + xsize)][1] > 240 and img[ro(y + ysize)][ro(x + xsize)][2] > 240:
            return False
    xsize = -Size
    ysize = -Size
    if 0 < (x + xsize) and x + xsize < img.shape[1] - 1 and 0 < (y + ysize) and y + ysize < img.shape[0] - 1:
        if img[ro(y + ysize)][ro(x + xsize)][0] > 240 and img[ro(y + ysize)][ro(x + xsize)][1] > 240 and img[ro(y + ysize)][ro(x + xsize)][2] > 240:
            return False
    xsize = 0
    ysize = 0
    if 0 < (x + xsize) and x + xsize < img.shape[1] - 1 and 0 < (y + ysize) and y + ysize < img.shape[0] - 1:
        if img[ro(y + ysize)][ro(x + xsize)][0] > 240 and img[ro(y + ysize)][ro(x + xsize)][1] > 240 and img[ro(y + ysize)][ro(x + xsize)][2] > 240:
            return False
    return True


def los(x1, y1, x2, y2, img):
    width = x2 - x1
    height = y2 - y1
    max_ = max(abs(width), abs(height))
    if max_ != 0:
        _height = height / max_
        _width = width / max_
        # print(f"{_width} {_height} {max_}")
        for i in range(int(max_)):
            # print(f"{x1 + i * _width} {y1 + i * _height} {img[y1 + i * _height][x1 + i * _width]}")
            if clear_(x1 + i * _width, y1 + i * _height, img) == False:
                return False
        return True
    elif width == 0:
        for i in range(int(height)):
            if clear_(x1, y1 + i * height, img) == False:
                return False
        return True
    elif height == 0:
        for i in range(int(width)):
            if clear_(x1 + i * width, y1, img) == False:
                return False
        return True


def samp(img):
    y = randrange(0, img.shape[0])
    x = randrange(0, img.shape[1])

    while clear_(x, y, img) == False:
        y = randrange(0, img.shape[0])
        x = randrange(0, img.shape[1])

    return x, y


def get_green(img):
    x, y = 0, 0
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i][j][0] < 50 and img[i][j][1] > 210 and img[i][j][2] < 50:
                x = j
                y = i
    return x, y


def get_red(img):
    x, y = 0, 0
    for i in range(img.shape[0] - 1, -1, -1):
        for j in range(img.shape[1] - 1, -1, -1):
            if img[i][j][0] < 50 and img[i][j][1] < 50 and img[i][j][2] > 240:
                x = j
                y = i
    return x, y


def ro(num):
    return int('{:.0f}'.format(num))
