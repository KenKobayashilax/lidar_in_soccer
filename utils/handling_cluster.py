import open3d as o3d
import numpy as np
import utils.visualizer as visualizer

#visualize by cluster according to labels. To check the label_id, please refer to the window name
def visualize_by_cluster(pcd, labels, colors=[1,0,0]):                             
    # Crop point clouds based on clusters
    unique_labels = np.unique(labels)

    for i, cluster_id in enumerate(unique_labels):
        if cluster_id == -1:
            # Skip outlier points (points not assigned to any cluster)
            continue
        
        cluster_cloud = pcd.select_by_index(np.where(np.array(labels)==cluster_id)[0])

        # Visualize the cropped cluster
        o3d.visualization.draw_geometries([cluster_cloud],
                                        window_name=f"cluster_{cluster_id}",
                                        width=800,
                                        height=600)

def visualize_by_cluster_bbox(pcd, labels, fl_labels, colors=[1,0,0]):                             
    # Crop point clouds based on clusters
    unique_labels = np.unique(labels)

    for cluster_id in fl_labels:
        cluster_cloud = pcd.select_by_index(np.where(np.array(labels)==cluster_id)[0])
        cluster_cloud.paint_uniform_color(colors)

        # Visualize the cropped cluster
        o3d.visualization.draw_geometries([cluster_cloud],
                                        window_name=f"cluster_{cluster_id}",
                                        width=800,
                                        height=600)
        
#crop (and save) the cluster corresponding to clluster id.
def crop_cluster(pcd, labels, cluster_id, visualize=False): 
    # Convert Open3D point cloud to numpy array
        pcd_np = np.asarray(pcd.points)
        
        # Extract points belonging to the current cluster
        cluster_points = pcd_np[labels==cluster_id]
        
        # Create a new Open3D point cloud for the cluster
        cropped_pcd = pcd.select_by_index(np.where(np.array(labels)==cluster_id)[0])
        cropped_pcd.paint_uniform_color([1,0,0])
        
        if visualize:
            # Visualize the cropped cluster
            o3d.visualization.draw_geometries([cropped_pcd],
                                            window_name=f"cluster_{cluster_id}",
                                            width=800,
                                            height=600)
        return(cropped_pcd)

def visualize_bbox_result(org_pcd, human_clusters,time_duration=0.2, cam_params=None, visualize=False):
    if human_clusters is not None: 
        org_pcd.paint_uniform_color([0,0,0])
        org_pcd_load = np.asarray(org_pcd.points)
        org_pcd_color = np.asarray(org_pcd.colors)

        human_pcd = o3d.geometry.PointCloud()
        human_pcd.points = o3d.utility.Vector3dVector(human_clusters)
        human_pcd.paint_uniform_color([1,0,0])
        human_pcd_color = np.asarray(human_pcd.colors)
        human_pcd_load = np.asarray(human_pcd.points)

        res_pcd = o3d.geometry.PointCloud()
        res_pcd_load = np.concatenate((human_pcd_load, org_pcd_load), axis=0)
        res_pcd_color = np.concatenate((human_pcd_color,org_pcd_color), axis=0) 
        res_pcd.points = o3d.utility.Vector3dVector(res_pcd_load)   
        res_pcd.colors = o3d.utility.Vector3dVector(res_pcd_color)       

        if visualize:
            visualizer.visualize(res_pcd, 
                                time_duration=time_duration, 
                                window_name="bbox_result", 
                                width=1920, 
                                height=1080, 
                                cam_params=cam_params)
