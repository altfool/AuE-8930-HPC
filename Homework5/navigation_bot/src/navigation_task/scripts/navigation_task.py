#!/usr/bin/env python
# convert between numpy & occupancy grid: https://github.com/eric-wieser/ros_numpy/blob/master/src/ros_numpy/occupancy_grid.py
# convert quaternion to (roll, pitch, yaw): https://answers.ros.org/question/290534/rotate-a-desired-degree-using-feedback-from-odometry/
import rospy
import os, math
import numpy as np
from PIL import Image
from nav_msgs.msg import OccupancyGrid, Odometry
from geometry_msgs.msg import Twist
from gridmap import OccupancyGridMap
from a_star_occupancy import a_star_occupancy
from collections import deque
from tf.transformations import euler_from_quaternion

# use dir "../tmp" to store all tmperory files,such as images, txt files, etc.
dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/tmp"
if not os.path.exists(dir_path):
  os.makedirs(dir_path)

# load parameters
starting_location = np.array(rospy.get_param("/starting_location").split(','),dtype=np.float32)
goal_location = np.array(rospy.get_param("/goal_location").split(','),dtype=np.float32)
robot_size = rospy.get_param("/robot_size")
map_resolution = rospy.get_param("/map_resolution")
linear_speed = rospy.get_param("/linear_speed")
rotate_speed = rospy.get_param("/rotate_speed")
distance_threshold = rospy.get_param("/distance_threshold")
angular_threshold = rospy.get_param("/angular_threshold")

_way_points = None

def inflate_map(mdata, inflate_size, val=100):
  """
    for simplicity, here i just inflate the map based on square of each pixel.
  """
  map_height, map_width = mdata.shape
  #original_val = mdata.max()
  occupied_pixel_indices = np.nonzero(mdata)
  for idx in range(len(occupied_pixel_indices[0])):
    curry = occupied_pixel_indices[0][idx]
    currx = occupied_pixel_indices[1][idx]
    for idxv in range(-inflate_size, inflate_size+1):
      for idxh in range(-inflate_size, inflate_size+1):
        tmpy = curry+idxv
        tmpx = currx+idxh
        if (0 <= tmpy < map_height) and (0 <= tmpx < map_width) and not mdata[tmpy, tmpx]:
          mdata[tmpy, tmpx] = val
  return mdata

def mapcallback(mdata):
  global _way_points
  # convert occupancy grid to numpy
  data = np.asarray(mdata.data, dtype=np.int8).reshape(mdata.info.height, mdata.info.width)
  data[data != 0] = 255
  raw_img = Image.fromarray(data, 'L')
  raw_img.save(dir_path+"/raw_map.png", "PNG")
  # inflate the map
  inflate_size = int(math.ceil(robot_size / map_resolution)) + 1
  inflated_data = inflate_map(np.copy(data), inflate_size)
  inflated_img = Image.fromarray(inflated_data, 'L')
  inflated_img.save(dir_path+"/inflated_map.png", "PNG")
  # do path planning using A* algorithm & save
  gmap = OccupancyGridMap(inflated_data, cell_size=map_resolution, occupancy_threshold=1)
  path, path_idx = a_star_occupancy(starting_location, goal_location, gmap, movement='8N')
  if not path:
    rospy.logerr("Goal is not reachable")
  _way_points = deque(path)
  print "way points: ", _way_points
  print "navigation plan idx: \n", path_idx
  with open(dir_path+'/navigation_plan.txt','w') as f:
    for waypoint in path_idx:
      line = ' '.join(str(ele) for ele in waypoint)
      f.write(line+'\n')
  rospy.loginfo("success")

def odomcallback2(msg):
  pass

def odomcallback(msg):
  global _way_points
  print "way points: ", _way_points
  #waypoints_len = len(_way_points)
  print msg.pose.pose.position
  orientation_q = msg.pose.pose.orientation
  orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
  (roll, pitch, yaw) = euler_from_quaternion(orientation_list)
  print "yaw: ", yaw
  movement = rospy.Publisher("/cmd_vel_mux/input/teleop", Twist, queue_size=10)
  mymsg = Twist()
  if _way_points:
    # check distance to next way point
    diff_x = _way_points[0][0]-msg.pose.pose.position.x
    diff_y = _way_points[0][1]-msg.pose.pose.position.y
    theta = math.atan2(diff_y, diff_x)
    dist = math.sqrt(diff_x**2+diff_y**2)
    if abs(yaw - theta) > angular_threshold:
      diff_angular = theta - yaw
      mymsg.angular.z = rotate_speed * diff_angular
      print "theta: ", theta
      print "diff_angular: ", diff_angular
    else:
      if dist < distance_threshold:
        _way_points.popleft()
        if _way_points:
          # move to 2nd way point
          diff_x = _way_points[0][0]-msg.pose.pose.position.x
          diff_y = _way_points[0][1]-msg.pose.pose.position.y
          #mymsg.linear.x = linear_speed
          theta = math.atan2(diff_y, diff_x)
          diff_angular = theta - yaw
          #mymsg.angular.z = min(rotate_speed, diff_angular)
          mymsg.angular.z = rotate_speed * diff_angular
          print "theta: ", theta
          print "diff_angular: ", diff_angular
      else:
        # continue to move to 1st way point
        mymsg.linear.x = min(linear_speed, dist)
  movement.publish(mymsg)


def listener():
  rospy.init_node("task", anonymous=True)
  rospy.Subscriber("/map", OccupancyGrid, mapcallback)
  rospy.Subscriber("/odom", Odometry, odomcallback)
  rospy.spin()

if __name__ == "__main__": listener()
