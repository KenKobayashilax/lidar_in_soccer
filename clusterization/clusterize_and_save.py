import pandas as pd
import numpy as np
import laspy
import open3d 
import pcl
import numpy as np
import laspy
import open3d as o3d

def cluster_dbscan(pcd_file, save_path=None):
    pcd = open3d.io.read_point_cloud(pcd_file)
    print(pcd)
    pcd = open3d.geometry.PointCloud(pcd)

    # eps is the clustering distance set, and min_points is the minimum number of points required to form a class
    labels = np.array(pcd.cluster_dbscan(eps=0.4, min_points=30, print_progress=True))
    max_label = max(labels)
    print(max_label)

    # randomly build n+1 colors, and normalize
    colors = np.random.randint(1, 255, size=(max_label + 1, 3)) / 255.
    colors = colors[labels]             # determines point's color according to its label
    colors[np.array(labels) < 0] = 0    # The noise configuration is black
    pcd.colors = open3d.utility.Vector3dVector(colors)  # Format conversion (because pcd.colors requires Vector3dVector format)

    # Visual point cloud list
    open3d.visualization.draw_geometries([pcd],
                                        window_name="cluster",
                                        width=800,
                                        height=600)
    if save_path != None:
        # 保存为 PCD 文件
        o3d.io.write_point_cloud(save_path, pcd)
    return pcd, labels, colors

#visualize by cluster according to labels. To check the label_id, please refer to the window name
def visualize_by_cluster(pcd, labels, colors=None):                             
    # Crop point clouds based on clusters
    unique_labels = np.unique(labels)

    for i, cluster_id in enumerate(unique_labels):
        if cluster_id == -1:
            # Skip outlier points (points not assigned to any cluster)
            continue
        
        # Convert Open3D point cloud to numpy array
        pcd_np = np.asarray(pcd.points)
        
        # Extract points belonging to the current cluster
        cluster_points = pcd_np[labels==cluster_id]
        

        # Create a new Open3D point cloud for the cluster
        cluster_cloud = o3d.geometry.PointCloud()
        cluster_cloud.points = o3d.utility.Vector3dVector(cluster_points)
        if colors is not None:
            min_index = np.argmax(labels==cluster_id)
            cluster_cloud.paint_uniform_color(colors[min_index])

        # Visualize the cropped cluster
        o3d.visualization.draw_geometries([cluster_cloud],
                                        window_name=f"cluster_{cluster_id}",
                                        width=800,
                                        height=600)

#crop (and save) the cluster corresponding to clluster id.
def crop_cluster(pcd, labels, cluster_id, save_path=None, Visualize=False): 
    # Convert Open3D point cloud to numpy array
        pcd_np = np.asarray(pcd.points)
        
        # Extract points belonging to the current cluster
        cluster_points = pcd_np[labels==cluster_id]
        
        # Create a new Open3D point cloud for the cluster
        cluster_cloud = o3d.geometry.PointCloud()
        cluster_cloud.points = o3d.utility.Vector3dVector(cluster_points)
        cluster_cloud.paint_uniform_color([1,0,0])
        
        if Visualize:
            # Visualize the cropped cluster
            o3d.visualization.draw_geometries([cluster_cloud],
                                            window_name=f"cluster_{cluster_id}",
                                            width=800,
                                            height=600)
        return cluster_cloud

def main():
    pcd_file = fr"C:/Users/15kob/Documents/study/abroad/lectures/LiDAR_in_soccer/data/New_data/New_data/test.pcd"
    save_path_for_clusters = None #save path for visualized all clusters
    save_path_for_cropped_cluster = None #save path for selected cluster
    
    #process dbscan (and save)
    pcd, labels, colors = cluster_dbscan(pcd_file, save_path=save_path_for_clusters)
    
    #visualize each cluster. Check window name to check the cluster number
    visualize_by_cluster(pcd, labels, colors)
    
    #select cluster id in comand line
    user_input = int(input("Please enter cluster id: "))
    
    #crop (and save) selected cluser
    crop_cluster(pcd, labels, cluster_id=user_input, save_path=save_path_for_cropped_cluster)

if __name__ == "__main__":
    main()
