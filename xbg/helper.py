import cv2
import matplotlib.pyplot as plt

threshold = 3000
path =  '/home/ittbmp014lw003/Documents/data/Exteroceptive-behaviour-generation'
record = 'robot_logger_device_2023_11_13_17_34_45/robot_logger_device_2023_11_13_17_34_45_realsense_depth'
sample = 'img_10120.png'
depth_img_name = f"{path}/{record}/{sample}"

depth_img = cv2.imread(depth_img_name, cv2.IMREAD_UNCHANGED)
print(depth_img)
depth_img[depth_img>threshold] = threshold
depth_img = depth_img/threshold

plt.gca().set_axis_off()
plt.imshow(depth_img)
plt.savefig('../static/depth.png', bbox_inches='tight', pad_inches=0)
