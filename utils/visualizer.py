import time
from networkx import caveman_graph
import open3d as o3d
import os
import cv2

def visualize(pcd_list, time_duration=100, window_name="cluster", width=1920, height=1080, cam_params=None):
    # 可視化ウィンドウを作成
    vis = o3d.visualization.Visualizer()
    vis.create_window(window_name=window_name, width=width, height=height, left=50, top=50, visible=True)

    if type(pcd_list)!=list:
        # ポイントクラウドを追加
        vis.add_geometry(pcd_list)
    else:
        for geometry in pcd_list:
            vis.add_geometry(geometry)
    
    if cam_params is not None:
        view_control = vis.get_view_control()
        view_control.convert_from_pinhole_camera_parameters(cam_params,allow_arbitrary=True)
    
    if time_duration is not None:
        # 描画
        vis.poll_events()
        vis.update_renderer()

        # 待機
        time.sleep(time_duration)

        # ウィンドウを閉じる
        vis.destroy_window()
    
    elif time_duration is None:
        vis.run()
    
'''
How to use?

cam_params = save_camera_params(pcd)
load_camera_params(pcd, cam_params)
'''

def save_camera_params(pcd):
    # make setting window
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    vis.add_geometry(pcd)
    view_control = vis.get_view_control()

    # wait for setting the view by user
    print("set the view point and close the window")
    vis.run()

    # save camera params
    cam_params = view_control.convert_to_pinhole_camera_parameters()
    vis.destroy_window()
    return cam_params

def load_camera_params(pcd, cam_params):
    # load camera params
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    vis.add_geometry(pcd)
    view_control = vis.get_view_control()
    view_control.convert_from_pinhole_camera_parameters(cam_params,allow_arbitrary=True)

    # 再現した視点で表示
    vis.run()
    vis.destroy_window()
    
def visualize_pcds(file_list, save_folder=None, time_duration=0.1, width=1920, height=1080, cam_params=None):
    vis = o3d.visualization.Visualizer()
    vis.create_window(window_name="window", width=width, height=height, left=50, top=50, visible=True)
    
    # geometry is the point cloud used in your animaiton
    geometry = o3d.geometry.PointCloud(o3d.io.read_point_cloud(file_list[0]))
    vis.add_geometry(geometry)
    if cam_params is not None:
        view_control = vis.get_view_control()
        view_control.convert_from_pinhole_camera_parameters(cam_params,allow_arbitrary=True)

    for pcd_file in file_list:
        # now modify the points of your geometry
        # you can use whatever method suits you best, this is just an example
        if save_folder is not None:
            save_path = save_folder + '/' + os.path.splitext(os.path.basename(pcd_file))[0] + '.png'
        
        geometry.points = o3d.io.read_point_cloud(pcd_file).points
        geometry.colors = o3d.io.read_point_cloud(pcd_file).colors
        vis.update_geometry(geometry)
        vis.poll_events()
        vis.update_renderer()
        vis.run()
        # 待機
        time.sleep(time_duration)
        if save_path is not None:
            vis.capture_screen_image(save_path, do_render=False)
    # ウィンドウを閉じる
    vis.destroy_window()
    
def save_video(image_folder, video_name, fps=10, step=1, start=0, end=-1):
    # Get the list of image files in the directory
    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]

    # Get image dimensions
    img = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, _ = img.shape

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(video_name, fourcc, fps, (width, height))

    # Loop through images and write to video
    for i in range(start, len(images)+end+1, step):
        image = images[i]
        img_path = os.path.join(image_folder, image)
        frame = cv2.imread(img_path)
        video.write(frame)

    # Release the VideoWriter
    video.release()