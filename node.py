from math import inf
import time
from helper import *
import cv2

PIPE = "/home/chaoticsaint/Desktop/KRSSG/3/catkin/src/turtcontrol/scripts/Pipe"


class Node():
    def __init__(self, img, copy, parent, x, y, tree, other):
        self.img = img
        self.parent = parent
        self.x = x
        self.y = y
        self.tree = tree
        self.kids = []
        self.other = other
        self.near = None
        self.step = 3
        self.copy = copy
        if self.parent == None:
            self.dis = 0
        else:
            self.dis = self.parent.dis + dist(self.x, self.y, self.parent.x, self.parent.y)
        self.go = 0
        self.connect = None

    def pick(self, xsamp, ysamp, id):
        width = xsamp - self.x
        height = ysamp - self.y
        max_ = max(abs(width), abs(height))
        if max_ != 0:
            _height = height / max_
            _width = width / max_
            for i in range(self.step, -1, -1):
                if los(self.x, self.y, self.x + i * _width, self.y + i * _height, self.img) == True:
                    y = int(self.y + i * _height)
                    x = int(self.x + i * _width)
        elif width == 0:
            for i in range(self.step, -1, -1):
                if los(self.x, self.y, self.x, self.y + i * height, self.img) == True:
                    x = int(self.x)
                    y = int(self.y + i * height)
        elif height == 0:
            for i in range(self.step, -1, -1):
                if los(self.x, self.y, self.x + i * width, self.y, self.img) == True:
                    x = int(self.x + i * width)
                    y = int(self.y)

        n = Node(self.img, self.copy, self, x, y, self.tree, self.other)
        cv2.line(self.copy, (self.x, self.y), (n.x, n.y), (0, 255, 0), 2)

        cv2.circle(self.copy, (n.x, n.y), 2, (255, 255, 0), -1)
        cv2.imshow("copy", self.copy)
        cv2.waitKey(1)
        self.kids.append(n)
        self.tree.append(n)

        # width = xsamp - self.x
        # height = ysamp - self.y
        # max_ = max(abs(width), abs(height))
        # if max_ != 0:
        #     _height = round(height / max_)
        #     _width = round(width / max_)
        #     for i in range(max_):
        #         print(los(self.x, self.y, xsamp - i * _width - 1, ysamp - i * _height - 1, self.img))
        #         if los(self.x, self.y, xsamp - i * _width - 1, ysamp - i * _height - 1, self.img) == True:
        #             n = Node(self.img, self.copy, self, xsamp - i * _width,
        #                      ysamp - i * _height, self.tree, self.other)
        # cv2.line(self.copy, (self.x, self.y), (xsamp - i * _width -
        #                                        1, ysamp - i * _height - 1), (0, 255, 0), 2)
        # # print("Picked")
        # cv2.circle(self.copy, (n.x, n.y), 2, (255, 255, 0), -1)
        # cv2.imshow("copy", self.copy)
        # cv2.waitKey(500)
        # self.kids.append(n)
        # self.tree.append(n)
        # self.near = nearest(n.x, n.y, self.other)
        #             return

        # width = xsamp - self.x
        # height = ysamp - self.y
        # max_ = max(abs(width), abs(height))
        # if max_ != 0:
        #     _height = round(height / max_)
        #     _width = round(width / max_)
        #     for i in range(self.step):
        #         print(los(self.x, self.y, self.x + i * _width, self.y + i * _height, self.img))
        #         if los(self.x, self.y, self.x + i * _width, self.y + i * _height, self.img) == True:
        #             n = Node(self.img, self.copy, self, self.x + i * _width,
        #                      self.y + i * _height, self.tree, self.other)
        #             cv2.line(self.copy, (self.x, self.y), (xsamp - i * _width -
        #                                                    1, ysamp - i * _height - 1), (0, 255, 0), 2)
        #             # print("Picked")
        #             cv2.circle(self.copy, (n.x, n.y), 2, (255, 255, 0), -1)
        #             cv2.imshow("copy", self.copy)
        #             cv2.waitKey(500)
        #             cv2.circle(self.copy, (n.x, n.y), 2, (255, 255, 0), -1)
        #             self.kids.append(n)
        #             self.tree.append(n)
        #             # print(self.tree)
        #             self.near = nearest(n.x, n.y, self.other)
        #             return

    def meetParent(self):
        # curr = self
        # while curr.parent != None:
        #     curr.go = 1
        #     cv2.line(self.copy, (curr.x, curr.y),
        #              (curr.parent.x, curr.parent.y), (0, 255, 255), 3)
        #     curr = curr.parent

        self.go = 1
        if self.parent != None:
            cv2.line(self.copy, (self.x, self.y),
                     (self.parent.x, self.parent.y), (0, 255, 255), 3)
            self.parent.meetParent()

    def rewire(self):
        if self.parent != self.tree[0] and self != self.tree[0]:
            min_ = inf
            for node in self.tree:
                if min_ > node.dis + dist(self.x, self.y, node.x, node.y) - self.dis and los(node.x, node.y, self.x, self.y, self.img) == True:
                    min_ = node.dis + dist(self.x, self.y, node.x, node.y) - self.dis
                    newParent = node
                    self.switchParent(self.parent, newParent)

    def switchParent(self, par1, par2):
        par1.kids.remove(self)
        par2.kids.append(self)
        self.dis = par2.dis + dist(self.x, self.y, par2.x, par2.y)
        self.parent = par2

    def found(self, node):
        self.connect = node
        print(self.connect.x, " ", self.connect.y)

    def list(self):
        curr = self
        with open(PIPE, 'w') as f:
            msg = f"{curr.x} {curr.y} \n"
            print("1         ", msg)
            f.write(msg)
        while True:
            k = 0
            for kid in curr.kids:
                if kid.go == 1:
                    k = 1
                    curr = kid
                    with open(PIPE, 'a') as f:
                        msg = f"{curr.x} {curr.y} \n"
                        print("1         ", msg)
                        f.write(msg)
                    continue
            if k != 1:
                break

        pre = curr
        curr = pre.connect
        while curr != None:
            with open(PIPE, 'a') as f:
                msg = f"{curr.x} {curr.y} \n"
                print("2                      ", msg)
                f.write(msg)
            curr = curr.parent

        # min_ = inf
        # for i in range(-self.step, self.step + 1):
        #     for j in range(-self.step, self.step + 1):
        #         # print(f"{i} {j}")
        #         # time.sleep(0.1)
        #         if min_ > dist(i, j, xsamp, ysamp):
        #             min_ = dist(i, j, xsamp, ysamp)
        #             xstate = i
        #             ystate = j
        #
        # # if id == 2:
        #     # print(min_, " ", los(self.x, self.y, xstate, ystate, self.img))
        # if los(self.x, self.y, xstate, ystate, self.img) == True:
        #     n = Node(self.img, self.copy, self, self.x + xstate,
        #              self.y + ystate, self.tree, self.other)
        #     cv2.line(self.copy, (self.x, self.y), (xstate, ystate), (0, 255, 0), 2)
        #     # print("Picked")
        #     cv2.circle(self.copy, (n.x, n.y), 2, (255, 0, 0), -1)
        #     cv2.imshow("copy", self.copy)
        #     cv2.waitKey(1)
        #     self.kids.append(n)
        #     self.tree.append(n)
        #     self.near = nearest(n.x, n.y, self.other)
