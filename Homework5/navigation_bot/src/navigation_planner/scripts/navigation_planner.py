#!/usr/bin/env python
# convert between numpy & occupancy grid: https://github.com/eric-wieser/ros_numpy/blob/master/src/ros_numpy/occupancy_grid.py
import rospy
import os, math
import numpy as np
from PIL import Image
from nav_msgs.msg import OccupancyGrid
from gridmap import OccupancyGridMap
from a_star_occupancy import a_star_occupancy

# use dir "../tmp" to store all tmperory files,such as images, txt files, etc.
dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/tmp"
if not os.path.exists(dir_path):
  os.makedirs(dir_path)

# load parameters
starting_location = np.array(rospy.get_param("/starting_location").split(','),dtype=np.float32)
goal_location = np.array(rospy.get_param("/goal_location").split(','),dtype=np.float32)
robot_size = rospy.get_param("/robot_size")
map_resolution = rospy.get_param("/map_resolution")
#print "{}\t{}\t{}\t{}".format(starting_location, goal_location, robot_size, map_resolution)
#print "{}\t{}\t{}\t{}".format(type(starting_location), type(goal_location), type(robot_size), type(map_resolution))

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

def callback(mdata):
  # convert occupancy grid to numpy
  data = np.asarray(mdata.data, dtype=np.int8).reshape(mdata.info.height, mdata.info.width)
  data[data != 0] = 255
  #data[data == 0] = 255
  raw_img = Image.fromarray(data, 'L')
  raw_img.save(dir_path+"/raw_map.png", "PNG")
  # inflate the map
  inflate_size = int(math.ceil(robot_size / map_resolution))
  inflated_data = inflate_map(np.copy(data), inflate_size)
  inflated_img = Image.fromarray(inflated_data, 'L')
  inflated_img.save(dir_path+"/inflated_map.png", "PNG")
  # do path planning using A* algorithm & save
  gmap = OccupancyGridMap(inflated_data, cell_size=map_resolution, occupancy_threshold=1)
  path, path_idx = a_star_occupancy(starting_location, goal_location, gmap, movement='8N')
  if not path:
    rospy.logerr("Goal is not reachable")
  print "navigation plan idx: \n", path_idx
  with open(dir_path+'/navigation_plan.txt','w') as f:
    for waypoint in path_idx:
      line = ' '.join(str(ele) for ele in waypoint)
      f.write(line+'\n')
  with open(dir_path+'/navigation_plan_coords.txt','w') as f:
    for waypoint in path:
      line = ' '.join(str(ele) for ele in waypoint)
      f.write(line+'\n')
  rospy.loginfo("success")

def listener():
  rospy.init_node("planner", anonymous=True)
  rospy.Subscriber("/map", OccupancyGrid, callback)
  rospy.spin()

if __name__ == "__main__": listener()
