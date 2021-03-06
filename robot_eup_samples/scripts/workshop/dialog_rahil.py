#!/usr/bin/env python
import rospy
import robot_eup
from robot_eup.msg import RobotType

#############################################

def main_loop(robot):

    robot.say(text='Welcome to the restaurant. How many people?')
    robot.display_message(
        message='Welcome to the restaurant. How many people?',
        duration=3)
    command = robot.wait_for_speech()
    robot.say(text='Okay, come with me')
    robot.move(x=0.5, y= 0.0, theta=0.5, duration=4)


#############################################

if __name__ == '__main__':
    rospy.init_node('robot_eup_dialog')
    robot = robot_eup.RobotFactory().build(RobotType.TURTLEBOT)
    robot.start_robot()
    while not rospy.is_shutdown():
        main_loop(robot)
