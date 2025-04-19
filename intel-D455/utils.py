# utils.py
import os
import datetime
import pyrealsense2 as rs

def get_depth_camera_info(profile):
    """
    获取深度相机的内参信息和深度值比例因子

    参数：
        pipeline: pipeline对象，已经初始化的深度相机

    返回值：
        depth_scale: 深度值的比例因子
        intrinsics: 深度图像的内参信息
    """
    depth_sensor = profile.get_device().first_depth_sensor()
    depth_stream = profile.get_stream(rs.stream.depth)
    depth_intrinsics = depth_stream.as_video_stream_profile().get_intrinsics()
    depth_scale = depth_sensor.get_depth_scale()
    print("Depth Scale is: ", depth_scale)
    print("Depth intrinsics:")
    print(f"Width: {depth_intrinsics.width}")
    print(f"Height: {depth_intrinsics.height}")
    print(f"PPX (principal point x): {depth_intrinsics.ppx}")
    print(f"PPY (principal point y): {depth_intrinsics.ppy}")
    print(f"FX (focal length x): {depth_intrinsics.fx}")
    print(f"FY (focal length y): {depth_intrinsics.fy}")
    print(f"Distortion model: {depth_intrinsics.model}")
    print(f"Distortion coefficients: {depth_intrinsics.coeffs}")

def create_camera_save_path(save_path=None):
    """
    创建保存并返回 D455 图像和深度信息的路径
    Args:
        save_path: 自定义路径, default=None, 默认运行文件的当前目录下

    Returns:
        color图存储路径, depth信息存储路径
    """
    if save_path is None:
        save_path = os.getcwd()
    time_path = f"{datetime.datetime.now():%Y_%m_%d_%H_%M_%S}".replace(":", "_")
    color_path = os.path.join(save_path, time_path, 'rgb')
    depth_path = os.path.join(save_path, time_path, 'depth')

    os.makedirs(color_path, exist_ok=True)
    os.makedirs(depth_path, exist_ok=True)
    return color_path, depth_path
