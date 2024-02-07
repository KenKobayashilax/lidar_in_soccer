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

def compute_nearest_multi_cluster(pcd, labels, center_prev_list): 
    #initialization
    nearest_cluster_id = 0
    nearest_center = np.zeros(3)
    nearest_dist = np.inf
    
    #get label values
    unique_labels = np.unique(labels)
    
    nearest_cluster_ids = []
    
    for center_prev in center_prev_list:
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
            
                nearest_cluster_ids.append(nearest_cluster_id)
    
    return nearest_cluster_ids


# compute bbox of clusters
def compute_bbox(pcd, labels):
    filtered_labels = []
    
    # convert to array
    points = np.asarray(pcd.points)
    
    #get label values
    unique_labels = np.unique(labels)
    
    bboxes = []
    
    for label in unique_labels:
        # extract the points belonging to the current clustering
        cluster_points = points[labels == label]

        # compute bbox
        if len(cluster_points) > 0:
            bbox_min = np.min(cluster_points, axis=0)
            bbox_max = np.max(cluster_points, axis=0)
        
            print(f"Cluster {label} Bounding Box:")
            
            bboxes.append({
                'label': label,
                'min': bbox_min,
                'max': bbox_max
            })
    
    for bbox in bboxes:
        # compute height, length and width of bbox
        height = bbox['max'][2] - bbox['min'][2]
        length = bbox['max'][0] - bbox['min'][0]
        width = bbox['max'][1] - bbox['min'][1]

        # check if bbox seems like a human
        if 1.3 <= height <= 2.2 and 0.2 <= length <= 2.5 and 0.2 <= width <= 2.5:
            filtered_labels.append(bbox['label'])
    
    print('filtered_labels:', filtered_labels)  
    
  
    human_red_pcd = change_multi_cluster_color(pcd, labels, filtered_labels, color=[1.0, 0.0, 0.0])
    #o3d.visualization.draw_geometries([human_red_pcd])
    
    
    return filtered_labels




#change color of only selected cluster
def change_cluster_color(pcd, labels, cluster_id, color=[1.0, 0.0, 0.0]):
    colors = np.asarray(pcd.colors)
    for i in range(len(labels)):
        if labels[i] == cluster_id:  
            colors[i] = color
    
    pcd.colors = o3d.utility.Vector3dVector(colors)
    
    return pcd



def change_multi_cluster_color(pcd, labels, cluster_id, color=[1.0, 0.0, 0.0]):
    colors = np.asarray(pcd.colors)
    for i in range(len(labels)):
        
        for id in cluster_id:
            if labels[i] == id:  
                colors[i] = color
    
    pcd.colors = o3d.utility.Vector3dVector(colors)
    
    return pcd