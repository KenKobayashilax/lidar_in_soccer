
import numpy as np
import open3d 
from settings import DATA_PATH
from utils import visualizer


#clusterize point clouds
def open3d_cluster(pcd, 
                   eps, #eps should be changed according to the distance to human.
                   visualize_noise, #visualize noise points or not.
                   window_name,
                   time_duration, #how long window is visualized
                   cam_params,
                   save_path,
                   visualize): 
    
    # pcd = open3d.geometry.PointCloud(pcd)
    
    # eps is the clustering distance set, and min_points is the minimum number of points required to form a class
    labels = pcd.cluster_dbscan(eps, min_points=30, print_progress=True)
    max_label = max(labels)
    print("num_clusters", max_label+1)
    
    # assert max_label==-1, "cluster was not found by db_scan.try again by higher eps!!"
    if max_label==-1:
        print("cluster was not found by db_scan!")
        return pcd, labels
    
    # randomly build n+1 colors, and normalize
    colors = np.random.randint(1, 255, size=(max_label + 1, 3)) / 255.
    colors = colors[labels]             # determines point's color according to its label
    colors[np.array(labels) < 0] = 0    # The noise configuration is black
    
    pcd.colors = open3d.utility.Vector3dVector(colors)  # Format conversion (because pcd.colors requires Vector3dVector format)
    
    # delete noise points
    if not visualize_noise:
        #select only clusterized points
        pcd_without_noise = pcd.select_by_index(np.where(np.array(labels) != -1)[0])
    else:
        pcd_without_noise = pcd
    
    if save_path != None:
        # save as .pcd file
        """this pcd file includes noise!!"""
        open3d.io.write_point_cloud(save_path, pcd)
    
    
    # close window at the time of selected time duration
    if visualize == True:
        if time_duration is not None:
            # Visual point cloud list
            visualizer.visualize([pcd_without_noise],time_duration=time_duration,
                                window_name=window_name,cam_params=cam_params)
        # normal window
        else: 
            open3d.visualization.draw_geometries([pcd_without_noise],
                                        window_name=window_name)
    return pcd, labels


# fit plane and delete points on the plane
def fit_plane(pcd, distance_threshold, visualize_plane):   
    #pcd = open3d.io.read_point_cloud(pcd_file)
    plane_model, inliers = pcd.segment_plane(distance_threshold,
                                            ransac_n=3,
                                            num_iterations=1000)
    [a, b, c, d] = plane_model
    print(f"Plane equation: {a:.2f}x + {b:.2f}y + {c:.2f}z + {d:.2f} = 0")

    inlier_cloud = pcd.select_by_index(inliers)
    inlier_cloud.paint_uniform_color([1.0, 0, 0])
    outlier_cloud = pcd.select_by_index(inliers, invert=True)
    
    if visualize_plane==True: #weather visualize plane fitting or not
        open3d.visualization.draw_geometries([inlier_cloud, outlier_cloud])
    
    return outlier_cloud

#one cycle of clustrization
def clusterize(pcd, distance_threshold=0.05, num_planes=2, visualize_plane=False,
               eps=0.3, window_name="cluster", visualize_noise=True,
               time_duration=None, cam_params=None, save_path=None,visualize = True
               ):
    
    #iterate fitting planes for "num_planes" times
    # for i in range(num_planes):
    #     pcd = fit_plane(pcd, distance_threshold, visualize_plane=visualize_plane)
    
    outlier_cloud = pcd
    pcd, labels = open3d_cluster(outlier_cloud, eps, visualize_noise, window_name, time_duration,cam_params, save_path, visualize)
    return pcd, labels

def main():
    pcd_file = rf'{DATA_PATH}/LIVOX_Hallway_pcds/Walking_to_end_1st1/res100ms_start30s/00100.pcd'
    eps=0.5
    num_planes=2 #how many times plane fitting is applied
    
    pcd = open3d.io.read_point_cloud(pcd_file)
    clusterize(pcd, eps=eps)
    
if __name__ == "__main__":
    main()
