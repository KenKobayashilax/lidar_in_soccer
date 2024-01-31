import open3d as o3d
import numpy as np

#compute the nearest cluster and output cluster id
def compute_nearest_cluster(pcd, labels, center_prev):
    #initialization
    nearest_cluster_id = 0
    nearest_center = np.zeros(3)
    nearest_dist = np.inf
    
    #get label values
    unique_labels = np.unique(labels)
    
    for i, cluster_id in enumerate(unique_labels):
        if cluster_id == -1:
            # Skip outlier points (points not assigned to any cluster)
            continue
        
        cropped_pcd = pcd.select_by_index(np.where(np.array(labels)==cluster_id)[0])
    
        #center of cropped_pcd
        center_tmp = cropped_pcd.get_center()
        #euclidian distance between center_prev and center_tmp
        current_dist = np.linalg.norm (center_prev - center_tmp)
        if current_dist < nearest_dist:
            nearest_dist = current_dist
            nearest_cluster_id = cluster_id
    
    
    return nearest_cluster_id

#change color of only selected cluster
def change_cluster_color(pcd, labels, cluster_id, color=[1.0, 0.0, 0.0]):
    colors = np.asarray(pcd.colors)
    for i in range(len(labels)):
        if labels[i] == cluster_id:  
            colors[i] = color
    
    pcd.colors = o3d.utility.Vector3dVector(colors)
    
    return pcd