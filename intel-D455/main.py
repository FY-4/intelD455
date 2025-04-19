# main.py
import pyrealsense2 as rs
import os
import cv2
import numpy as np
from utils import get_depth_camera_info, create_camera_save_path


saved_count = 0
extend_num = 3
width = 640
height = 480
fps = 30

color_path, depth_path = create_camera_save_path()
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, width, height, rs.format.z16, fps)
config.enable_stream(rs.stream.color, width, height, rs.format.bgr8, fps)

profile = pipeline.start(config)
get_depth_camera_info(profile)

try:
    while True:
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # 获取深度信息，以米为单位
        depth_scale = profile.get_device().first_depth_sensor().get_depth_scale()
        depth_image_in_meters = depth_image * depth_scale

        # 将无效的深度值设置为NaN
        depth_image_in_meters[depth_image == 0] = np.nan

        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
        images = np.hstack((color_image, depth_colormap))
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', images)
        key = cv2.waitKey(1)

        if key & 0xFF == ord('s'):
            saved_count += 1
            print(f"{saved_count} 已保存图像至 {color_path} 和 {depth_path}")
            cv2.imwrite(os.path.join(color_path, "{}.png".format(saved_count)), color_image)
            # 深度信息保存为 .npy 格式，单位为米
            np.save(os.path.join(depth_path, "{}.npy".format(saved_count)), depth_image_in_meters)
        elif key & 0xFF == ord('q') or key == 27:
            cv2.destroyAllWindows()
            break

finally:
    pipeline.stop()
