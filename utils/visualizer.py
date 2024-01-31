import time
import open3d as o3d

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