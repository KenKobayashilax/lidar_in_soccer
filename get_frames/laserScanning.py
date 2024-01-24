
import pandas as pd
import numpy as np
import laspy
import open3d 



def open3d_cluster(pcd_file):
    # Read the point cloud file
    pcd = open3d.io.read_point_cloud(pcd_file)
    print(pcd)
    pcd = open3d.geometry.PointCloud(pcd)

    # eps is the clustering distance set, and min_points is the minimum number of points required to form a class
    labels = pcd.cluster_dbscan(eps=0.6, min_points=30, print_progress=True)
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

'''
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

# Read point cloud data
point_cloud = open3d.io.read_point_cloud("D:/TUM File/semester5/pratical laser scanning/data/Measurement data/livox/New_data/23.pcd")
points = np.asarray(point_cloud.points)


# Check if the point cloud is non-empty before applying StandardScaler
if points.shape[0] > 0:
    # Optional: Standardize the point cloud for better DBSCAN performance
    scaler = StandardScaler()
    scaled_points = scaler.fit_transform(points)

    # Apply DBSCAN for clustering
    epsilon = 0.1
    min_samples = 10
    dbscan = DBSCAN(eps=epsilon, min_samples=min_samples)
    labels = dbscan.fit_predict(scaled_points)

    # Check if there are clusters
    if np.max(labels) >= 0:
        # Create Open3D color map
        colors = np.random.rand(np.max(labels) + 1, 3)
        colors[labels == -1] = [0, 0, 0]

        # Visualize the clustered point cloud
        point_cloud.colors = open3d.utility.Vector3dVector(colors[labels])
        open3d.visualization.draw_geometries([point_cloud])
    else:
        print("No clusters found.")
else:
    print("Point cloud is empty.")
''' 
    
pcd_file=fr"C:/Users/15kob/Documents/study/abroad/lectures/LiDAR_in_soccer/data/New_data/New_data/27.pcd"
open3d_cluster(pcd_file)


