#!/usr/bin/env python


import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from PID import PID
import math
import cv2

PIPE = "catkin/src/turtcontrol/scripts/Pipe"


class turtle_PID():

    def __init__(self):

        self.pub = rospy.Publisher('turtle1/cmd_vel', Twist, queue_size=10)
        rospy.Subscriber("turtle1/pose", Pose, self.pose_callback)

        rospy.init_node('turtle_controller', anonymous=True)
        self.rate = rospy.Rate(10)  # 10hz

        self.angle_PID = PID()
        self.distance_PID = PID()

        self.angle_PID.setKp(1.4)
        self.angle_PID.setKi(0)
        self.angle_PID.setKd(0)

        self.distance_PID.setKp(1.4)
        self.distance_PID.setKi(0)
        self.distance_PID.setKd(0)

        self.msg = Twist()

        self.move_turtle()

    def angular_controller(self, goal):

        self.R = math.sqrt(math.pow(self.current_pose_x - goal[0], 2) +
                           math.pow(self.current_pose_y - goal[1], 2))

        self.xr = self.R*math.cos(self.current_angle)
        self.yr = self.R*math.sin(self.current_angle)

        self.xim = self.current_pose_x + self.xr
        self.yim = self.current_pose_y + self.yr

        self.C = math.sqrt(math.pow(self.xim - goal[0], 2) +
                           math.pow(self.yim - goal[1], 2))

        if self.xim > goal[0]:

            self.alpha = math.acos(
                (2*math.pow(self.R, 2) - math.pow(self.C, 2))/(2*math.pow(self.R, 2)))
        else:
            self.alpha = 2*3.14*math.acos((2*math.pow(self.R, 2) -
                                           math.pow(self.C, 2))/(2*math.pow(self.R, 2)))

        print self.alpha
        while self.alpha > 0.005:
            self.R = math.sqrt(math.pow(self.current_pose_x - goal[0], 2) +
                               math.pow(self.current_pose_y - goal[1], 2))
            # print "dentro do while"
            self.xr = self.R*math.cos(self.current_angle)
            self.yr = self.R*math.sin(self.current_angle)

            self.xim = self.current_pose_x + self.xr
            self.yim = self.current_pose_y + self.yr

            self.C = math.sqrt(math.pow(self.xim - goal[0], 2) +
                               math.pow(self.yim - goal[1], 2))

            if self.xim > goal[0]:

                self.alpha = math.acos(
                    (2*math.pow(self.R, 2) - math.pow(self.C, 2))/(2*math.pow(self.R, 2)))

            else:

                self.alpha = 2*3.14 * \
                    math.acos((2*math.pow(self.R, 2) - math.pow(self.C, 2))/(2*math.pow(self.R, 2)))

            self.alpha = math.acos(
                (2*math.pow(self.R, 2) - math.pow(self.C, 2))/(2*math.pow(self.R, 2)))

            self.PID_angle = self.angle_PID.update(self.alpha)

            self.msg.angular.z = self.PID_angle

            self.pub.publish(self.msg)
        self.msg.angular.z = 0
        self.pub.publish(self.msg)

    def distance_controller(self, goal):

        self.distance = math.sqrt(math.pow(goal[0] - self.current_pose_x,
                                           2) + math.pow(goal[1] - self.current_pose_y, 2))
        #self.R = math.sqrt(math.pow(self.current_pose_x - goal[0] , 2) + math.pow(self.current_pose_y - goal[1] , 2))
        print "distance: " + str(self.distance)
        while self.distance > 0.1:

            self.distance = math.sqrt(
                math.pow(goal[0] - self.current_pose_x, 2) + math.pow(goal[1] - self.current_pose_y, 2))

            self.PID_distance = self.distance_PID.update(self.distance)

            self.msg.linear.x = self.PID_distance

            self.pub.publish(self.msg)
        self.msg.linear.x = 0
        self.pub.publish(self.msg)

    def get_user_input(self):

        with open(PIPE, 'r') as f:
            coords = f.readlines()

        self.goals = []
        for cord in coords:
            s = cord.split()
            p = [float(s[0])/60, 10 - float(s[1])/60]
            self.goals.append(p)

    def move_turtle(self):

        self.get_user_input()

        for goal in self.goals:
            print goal
            self.angular_controller(goal)

            self.distance_controller(goal)

    def pose_callback(self, data):

        self.current_pose_x = data.x
        self.current_pose_y = data.y
        self.current_angle = data.theta


if __name__ == '__main__':

    try:

        turtle_PID()

    except rospy.ROSInterruptException:

        pass
