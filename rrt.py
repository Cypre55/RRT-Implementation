import cv2
from random import randrange
from math import inf
import time
from node import *
from helper import *


def rrt_connect(start, end, nodes, img, copy_, _copy):
    tree1 = []
    tree2 = []
    tree1.append(Node(img, copy_, None, start[0], start[1], tree1, tree2))
    tree2.append(Node(img, copy_, None, end[0], end[1], tree2, tree1))
    print("Started")

    while len(tree1) + len(tree2) < nodes + 2:
        x, y = samp(img)
        t = nearest(x, y, tree1)
        # print(t.tree)
        # time.sleep(0.2)
        t.pick(x, y, 1)
        cv2.circle(copy_, (x, y), 1, (255, 182, 193), -1)

        x, y = samp(img)
        b = nearest(x, y, tree2)
        # print(b.tree)
        # time.sleep(0.2)
        b.pick(x, y, 2)
        # b.rewire()
        # t.rewire()

        cv2.circle(copy_, (x, y), 1, (255, 182, 193), -1)

        near1 = nearest(tree2[-1].x, tree2[-1].y, tree1)
        near2 = nearest(tree1[-1].x, tree1[-1].y, tree2)
        # near = near1
        # mem = tree2[-1]
        # if dist(near2.x, near2.y, tree1[-1].x, tree1[-1].y) + near2.dis < dist(near1.x, near1.y, tree2[-1].x, tree2[-1].y) + near1.dis:
        #     near = near2
        #     mem = tree1[-1]
        if los(tree2[-1].x, tree2[-1].y, near1.x, near1.y, img) == True:
            near1.found(tree2[-1])
            tree2[-1].found(near1)
            print("Path Found!")
            printTree(tree1, copy_, (0, 0, 255))
            printTree(tree2, copy_, (255, 0, 0))
            printTree(tree1, _copy, (0, 0, 255))
            printTree(tree2, _copy, (255, 0, 0))
            drawPath(tree2[-1], near1)
            cv2.line(copy_, (tree2[-1].x, tree2[-1].y),
                     (near1.x, near1.y), (0, 255, 255), 3)
            print(f"Path found after {len(tree1) + len(tree2) - 2} nodes.")
            # cv2.imshow("Trees", _copy)
            # cv2.imshow("Path", copy_)
            tree1[0].list()
            return
        elif los(tree1[-1].x, tree1[-1].y, near2.x, near2.y, img) == True:
            near2.found(tree1[-1])
            tree1[-1].found(near2)
            print("Path Found!")
            printTree(tree1, copy_, (0, 0, 255))
            printTree(tree2, copy_, (255, 0, 0))
            printTree(tree1, _copy, (0, 0, 255))
            printTree(tree2, _copy, (255, 0, 0))
            drawPath(tree1[-1], near2)
            cv2.line(copy_, (tree1[-1].x, tree1[-1].y),
                     (near2.x, near2.y), (0, 255, 255), 3)
            print(f"Path found after {len(tree1) + len(tree2) - 2} nodes.")
            # cv2.imshow("Trees", _copy)
            # cv2.imshow("Path", copy_)
            tree1[0].list()
            return

    print("Path Not found!")
    printTree(tree1, copy_, (0, 0, 255))
    printTree(tree2, copy_, (255, 0, 0))


img = cv2.imread('tut.jpg')
# img = cv2.ellipse(img, (300, 300), (150, 150), 0,
#                   -10, 120, (255, 255, 255), 40)
copy_ = img.copy()
_copy = img.copy()
# g = get_green(img)
# r = get_red(img)

rrt_connect([54, 45], [540, 558], 3000, img, copy_, _copy)
# print(los(84, 70, 200, 70, img))
# cv2.line(copy_, (84, 70), (200, 70), (0, 255, 255), 1)


cv2.imshow("Trees", _copy)
cv2.imshow("Path", copy_)

cv2.waitKey(0)
cv2.destroyAllWindows()
