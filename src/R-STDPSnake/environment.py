import sys
import rospy

import math
import time
import numpy as np
from scipy import interpolate
from operator import itemgetter

from std_msgs.msg import Int8MultiArray, Float32, Bool
from std_msgs.msg._Float32MultiArray import Float32MultiArray
from geometry_msgs.msg import Transform

from parameters import *
from numpy import short
from pkg_resources import add_activation_listener


"""
    This controller is based on RSTDP controller developed by @Clamesc https://github.com/clamesc
"""


class VrepEnvironment():
    def __init__(self):
        self.pos_data = np.array([0,0])
        self.distance = 0
        self.delta = 0
        self.dvs_data = np.array([0,0])
        
        """Proximity sensor numpy arrays of 2 doubles"""
        
        self.forward_proxy_data = np.zeros(2, np.double)
        self.left_proxy_data = np.zeros(2, np.double)
        self.right_proxy_data = np.zeros(2, np.double)
        self.midLeft_proxy_data = np.zeros(2, np.double)
        self.midRight_proxy_data = np.zeros(2, np.double)
#         self.left25_proxy_data = np.zeros(2, np.double)
#         self.right25_proxy_data = np.zeros(2, np.double)
#         self.left55_proxy_data = np.zeros(2, np.double)
#         self.right55_proxy_data = np.zeros(2, np.double)

        """ROS subscribers"""

        self.dvsSub = rospy.Subscriber('dvsData', Int8MultiArray, self.dvs_callback)
        self.posSub = rospy.Subscriber('transformData', Transform, self.pos_callback)
        self.forwardProxySub = rospy.Subscriber('forwardProxyData', Float32MultiArray, self.forward_proxy_callback)
        self.leftProxySub = rospy.Subscriber('leftProxyData', Float32MultiArray, self.left_proxy_callback)
        self.rightProxySub = rospy.Subscriber('rightProxyData', Float32MultiArray, self.right_proxy_callback)
        self.midLeftProxySub = rospy.Subscriber('midLeftProxyData', Float32MultiArray, self.midLeft_proxy_callback) 
        self.midRightProxySub = rospy.Subscriber('midRightProxyData', Float32MultiArray, self.midRight_proxy_callback)
        self.collisionSub = rospy.Subscriber('collision', Bool, self.collision_cb)
        self.simStoppedSub = rospy.Subscriber('simStopped', Bool, self.simStopped_cb)
#         self.left25ProxySub = rospy.Subscriber('left25ProxyData', Float32MultiArray, self.left25_proxy_callback)
#         self.right25ProxySub = rospy.Subscriber('right25ProxyData', Float32MultiArray, self.right25_proxy_callback)
#         self.left55ProxySub = rospy.Subscriber('left55ProxyData', Float32MultiArray, self.left55_proxy_callback) 
#         self.right55ProxySub = rospy.Subscriber('right55ProxyData', Float32MultiArray, self.right55_proxy_callback)
        
        """ROS publishers"""

        self.radiusPub = rospy.Publisher('radius', Float32, queue_size=1)
        self.directionPub = rospy.Publisher('direction', Bool, queue_size=None)
        self.reset_pub = rospy.Publisher('resetRobot', Bool, queue_size=None)
        rospy.init_node('dvs_controller')
        self.rate = rospy.Rate(rate)

        self.steps = 0
        self.radius_pre = radius_max
        self.radius_buffer = 0
        self.turn_pre = 0.
        self.collisionInSim = False
        self.simStopped = False
        self.resize_factor = [dvs_resolution[0]//resolution[0], dvs_resolution[1]//resolution[1]]

    def dvs_callback(self, msg):
        self.dvs_data = msg.data
        return
    
    """
        Unused:    Performs distance traveled calculations and saves distance, position and distance delta
    """
    
    def pos_callback(self, msg):
        pos_temp = np.array([msg.translation.x, msg.translation.y])
        self.delta = np.linalg.norm(pos_temp - self.pos_data)
        self.distance += self.delta
        self.pos_data = pos_temp
        return

    """
        Proximity sensors callbacks.
        If sensor does not encounter anything, set distance data to maximum sensing distance
    """

    def forward_proxy_callback(self, msg):
        self.forward_proxy_data[0] = msg.data[0]
        if msg.data[0] > 0:
            self.forward_proxy_data[1] = msg.data[1]
        else:
            self.forward_proxy_data[1] = 1.0
        return
    
    def left_proxy_callback(self, msg):
        self.left_proxy_data[0] = msg.data[0]
        if msg.data[0] > 0:
            self.left_proxy_data[1] = msg.data[1]
        else:
            self.left_proxy_data[1] = 1.5
        return
    
    def right_proxy_callback(self, msg):
        self.right_proxy_data[0] = msg.data[0]
        if msg.data[0] > 0:
            self.right_proxy_data[1] = msg.data[1]
        else:
            self.right_proxy_data[1] = 1.5
        return
    
    def midLeft_proxy_callback(self, msg):
        self.midLeft_proxy_data[0] = msg.data[0]
        if msg.data[0] > 0:
            self.midLeft_proxy_data[1] = msg.data[1]
        else:
            self.midLeft_proxy_data[1] = 1.1
        return
     
    def midRight_proxy_callback(self, msg):
        self.midRight_proxy_data[0] = msg.data[0]
        if msg.data[0] > 0:
            self.midRight_proxy_data[1] = msg.data[1]
        else:
            self.midRight_proxy_data[1] = 1.1
        return
#     
#     def left25_proxy_callback(self, msg):
#         if msg.data[0] > 0:
#             self.left25_proxy_data[0] = msg.data[0]
#             self.left25_proxy_data[1] = msg.data[1]
#             u = self.left25_proxy_data[1]
#         else:
#             u = 6.4
#         return
#     
#     def right25_proxy_callback(self, msg):
#         if msg.data[0] > 0:
#             self.right25_proxy_data[0] = msg.data[0]
#             self.right25_proxy_data[1] = msg.data[1]
#             u = self.right25_proxy_data[1]
#         else:
#             u = 6.4
#         return
#     
#     def left55_proxy_callback(self, msg):
#         if msg.data[0] > 0:
#             self.left55_proxy_data[0] = msg.data[0]
#             self.left55_proxy_data[1] = msg.data[1]
#             u = self.left55_proxy_data[1]
#         else:
#             u = 6.4
#         return
#     
#     def right55_proxy_callback(self, msg):
#         if msg.data[0] > 0:
#             self.right55_proxy_data[0] = msg.data[0]
#             self.right55_proxy_data[1] = msg.data[1]
#             u = self.right55_proxy_data[1]
#         else:
#             u = 6.4
#         return

    def simStopped_cb(self, msg):
        self.simStopped = msg.data

    def collision_cb(self, msg):
        self.collisionInSim = msg.data

    def reset(self):
        self.radiusPub.publish(100.)
        self.radius_pre = 100.
        self.distance = 0.
        self.reset_pub.publish(Bool(True))
        time.sleep(1)
        return np.zeros((resolution[0],resolution[1]),dtype=int), 0., 0., 0., 0.

    """
        1. Calculate radius
        2. Publish radius
        3. Calculate reward and state
        4. If collision occured, reset
        5. If training is over, save data
    """

    def step(self, n_l, n_r):
        
        self.steps += 1
        t = False

        self.radius_pre = n_r - n_l
        
        if (self.steps % 5 != 0):
            self.radius_buffer = self.radius_buffer + self.radius_pre
        else:
            self.radius_pre = self.radius_buffer/5.0
            self.radius_buffer = 0

        if self.radius_pre == 0:
            self.radius_pre = radius_max
        self.radiusPub.publish(self.radius_pre)
        self.rate.sleep()

        rc = 0.0
#         r = self.getAreaBasedReward()
        r, d_l, d_r = self.getAreaBasedReward()
        s = self.getState()
        
        if self.simStopped:
            return s, r, rc, t, self.steps, self.simStopped, self.distance, d_l, d_r
#         print("Radius ", self.radius_pre)
#         print("reward ", r)
        
        
        if self.collisionInSim:
            self.steps = 0
            t = True
            self.reset()
#             print ("collision: ", rc)
            return s,r,rc,t, self.steps, self.simStopped, self.distance, d_l, d_r
        
        
        return s,r,rc,t, self.steps, self.simStopped, self.distance, d_l, d_r

    """
        Approximates center by projecting outter left and right sensor distance on 
        presumed x plane.
    """

    def getApproxCenterDistanceReward(self):
#         interpolateLeft = []
#         interpolateRight = []
# 
#         interpolateLeft.append((0.0, self.forward_proxy_data[1]))
#         interpolateLeft.append((math.cos(math.pi / 3) * self.left55_proxy_data[1], math.sin(math.pi / 3) * self.left55_proxy_data[1]))
#         interpolateLeft.append((math.cos(math.pi / 4) * self.midLeft_proxy_data[1], math.sin(math.pi / 4) * self.midLeft_proxy_data[1]))
#         interpolateLeft.append((math.cos(math.pi / 6) * self.left25_proxy_data[1], math.sin(math.pi / 6) * self.left25_proxy_data[1]))
#         interpolateLeft.append((self.left_proxy_data[1], 0))
#         
#         interpolateRight.append((0.0, self.forward_proxy_data[1]))
#         interpolateRight.append((math.cos(math.pi / 3) * self.right55_proxy_data[1], math.sin(math.pi / 3) * self.right55_proxy_data[1]))
#         interpolateRight.append((math.cos(math.pi / 4) * self.midRight_proxy_data[1], math.sin(math.pi / 4) * self.midRight_proxy_data[1]))
#         interpolateRight.append((math.cos(math.pi / 6) * self.right25_proxy_data[1], math.sin(math.pi / 6) * self.right25_proxy_data[1]))
#         interpolateRight.append((self.right_proxy_data[1], 0))
# 
#         leftx, lefty = zip(*sorted(interpolateLeft, key=itemgetter(0)))
#         rightx, righty = zip(*sorted(interpolateRight, key=itemgetter(0)))
#         
#         leftSplines = interpolate.InterpolatedUnivariateSpline(leftx, lefty)
#         rightSplines = interpolate.InterpolatedUnivariateSpline(rightx, righty)
#         
#         areaLeft = leftSplines.integral(0, max(leftx))
#         areaRight = rightSplines.integral(0, max(rightx))

        #r = max(self.left_proxy_data[1], self.right_proxy_data[1])
        
        r = 0.0
#         shortestWhisker = min(self.left_proxy_data[1], self.right_proxy_data[1])
#         
#         r = (shortestWhisker + 3) / ((shortestWhisker ** 3) + 1) - 0.45  
        

        distanceLeft = self.left_proxy_data[1] * math.cos(0.872665)
        distanceRight = self.right_proxy_data[1] * math.cos(0.872665)
        
        r = (((distanceRight + distanceLeft) / 2) - distanceLeft) ** 3
        
        return r, distanceLeft, distanceRight
    
    """Calculates reward based on triangle area between sensed distances
                   Does not operate on center assumption
    """
    
    def getAreaBasedReward(self):
#         leftSectorArea = (1 ** 2) * (0.87266) / 2.0
#         rightSectorArea = (1 ** 2) * (0.87266) / 2.0
#         
#         leftTriangle = 0.5 * 1.0 * 1.5 * math.sin(0.87266)
#         rightTriangle = 0.5 * 1.0 * 1.5 * math.sin(0.87266)
#         leftBaseTriangle = 0.5 * self.left_proxy_data[1]  * distanceLeft * math.cos(0.698132)
#         rightBaseTriangle = 0.5 * self.right_proxy_data[1] * distanceRight * math.cos(0.698132)
#         
#         inverseLeftArea = leftTriangle - leftOutterTriangleArea - leftInnerTriangleArea
#         inverseRightArea = rightTriangle - rightOutterTriangleArea - rightInnerTriangleArea
        r = 0.0
        
        leftOutterTriangleArea = 0.5 * self.left_proxy_data[1] * self.midLeft_proxy_data[1] * math.sin(0.43633) 
        leftInnerTriangleArea = 0.5 * self.forward_proxy_data[1] * self.midLeft_proxy_data[1] * math.sin(0.43633)
        
        rightOutterTriangleArea = 0.5 * self.right_proxy_data[1] * self.midRight_proxy_data[1] * math.sin(0.43633) 
        rightInnerTriangleArea = 0.5 * self.forward_proxy_data[1] * self.midRight_proxy_data[1] * math.sin(0.43633)
        
        leftArea = leftOutterTriangleArea + leftInnerTriangleArea
        rightArea = rightOutterTriangleArea + rightInnerTriangleArea
        
        r = (rightArea - leftArea) ** 3

        return r, leftArea, rightArea
    """Unused: clipping to 0 - 1.0 interval for interpolation"""
    
    def clip(self, n):
        return max(0.0, min(n, 1.0))

    """Rescale dvs resolution to defined in params, credit to @Clamesc"""
    
    def getState(self):
        new_state = np.zeros((resolution[0],resolution[1]),dtype=int)
        for i in range(len(self.dvs_data)//2):
            try:
                if crop_bottom <= self.dvs_data[i*2+1] < (dvs_resolution[1]-crop_top):
                    idx = ((self.dvs_data[i*2])//self.resize_factor[0], (self.dvs_data[i*2+1]-crop_bottom)//self.resize_factor[1])
                    new_state[idx] += 1
            except:
                pass
        return new_state