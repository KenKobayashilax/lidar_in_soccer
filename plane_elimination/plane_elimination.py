import open3d
import numpy as np
from plane_elimination.plane_equotions_list import planes_list, bool_list

#eliminate points by only one plane
def eliminate_one_plane(pcd, 
                    plane, #coefficients_list of planes [a,b,c,d] -> ax+by+cz+d=0
                    smaller=True, #equotion is whether < or >
                    visualize=True): #visualize each plane
    a, b, c, d = plane
    points = np.asarray(pcd.points)
    values = a * points[:, 0] + b * points[:, 1] + c * points[:, 2] + d
    
    # Select points fulfilling the equation of the plane
    if smaller:
        inliers = np.where(values < 0)[0]
    else:
        inliers = np.where(values > 0)[0]

    # Visualize the selected points
    inlier_cloud = pcd.select_by_index(inliers)
    outlier_cloud = pcd.select_by_index(inliers, invert=True)
    outlier_cloud.paint_uniform_color([1.0, 0, 0])

    if visualize:
        open3d.visualization.draw_geometries([inlier_cloud, outlier_cloud])
    return inlier_cloud

#eliminate points by several planes
def eliminate_planes(pcd, planes_list, bool_list, visualize=False):
    
    #eliminate outliers the plane by plane
    for plane, bool in zip(planes_list, bool_list):
        pcd = eliminate_one_plane(pcd=pcd, plane=plane, smaller=bool, visualize=False)

    #visualize the result
    if visualize:
        open3d.visualization.draw_geometries([pcd])
    
    return pcd