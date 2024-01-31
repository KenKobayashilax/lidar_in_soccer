import open3d as o3d
import numpy as np

#visualize by cluster according to labels. To check the label_id, please refer to the window name
def visualize_by_cluster(pcd, labels, colors=None):                             
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