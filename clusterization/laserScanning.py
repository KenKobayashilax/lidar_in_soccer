
import pandas as pd
import numpy as np
import laspy
import open3d 



def open3d_cluster(pcd):
    # Read the point cloud file
    #pcd = open3d.io.read_point_cloud(pcd_file)
    print(pcd)
    pcd = open3d.geometry.PointCloud(pcd)

    # eps is the clustering distance set, and min_points is the minimum number of points required to form a class
    labels = pcd.cluster_dbscan(eps=0.3, min_points=30, print_progress=True)
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



def fit_plane(pcd):   
    #pcd = open3d.io.read_point_cloud(pcd_file)
    plane_model, inliers = pcd.segment_plane(distance_threshold=0.01,
                                            ransac_n=3,
                                            num_iterations=1000)
    [a, b, c, d] = plane_model
    print(f"Plane equation: {a:.2f}x + {b:.2f}y + {c:.2f}z + {d:.2f} = 0")

    inlier_cloud = pcd.select_by_index(inliers)
    inlier_cloud.paint_uniform_color([1.0, 0, 0])
    outlier_cloud = pcd.select_by_index(inliers, invert=True)
    open3d.visualization.draw_geometries([inlier_cloud, outlier_cloud],
                                    zoom=0.8,
                                    front=[-0.4999, -0.1659, -0.8499],
                                    lookat=[2.1813, 2.0619, 2.0999],
                                    up=[0.1204, -0.9852, 0.1215])
    
    return outlier_cloud
    


  
pcd_file='D:/TUM File/semester5/pratical laser scanning/data/Measurement data/Fieldtest Sport-Campus/New folder/test.pcd'

pcd = open3d.io.read_point_cloud(pcd_file)
outlier_cloud = fit_plane(pcd)
outlier_cloud2 = fit_plane(outlier_cloud)

open3d_cluster(outlier_cloud2)


