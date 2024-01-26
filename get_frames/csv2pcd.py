import csv
import open3d as o3d
import os
from settings import DATA_PATH

# Open the CSV file and read it line by line
def read_csv(csv_file_path,
             res=10, #res: time resolution
             start=0 #start: the time(second) to set as frame0 
             ):  
    with open(csv_file_path, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        

        # Create a dictionary to accumulate points for each timestamp
        points_by_timestamp = {}
        # Dictionary to correspond timestamp and saved name
        timestamp_list = {}

        # Iterate through the CSV rows and accumulate points
        frame_id = 0
        for i, row in enumerate(csvreader):
            timestamp = int(row['Timestamp'])
            if i==0:
                timestamp_lower_bound = int(timestamp) + start*1000000000 #set initial lower bound.
                timestamp_list[str(frame_id)] = timestamp_lower_bound
                points_by_timestamp[str(frame_id)] = []
                
            if timestamp - timestamp_lower_bound < 0: #the case timestamp doesn't reach frame0 
                continue
            
            x, y, z = float(row['X']), float(row['Y']), float(row['Z'])

            # Skip rows where X, Y, and Z values are all zero
            if x == 0 and y == 0 and z == 0:
                continue
            # Append the point to the list for the corresponding timestamp
            if timestamp - timestamp_lower_bound > res * 1000000: #unit of timestamp is 1 nano second(1/10^9 second)
                print("processing timestamp:",timestamp)
                timestamp_lower_bound += res * 1000000 #add time resolution to lower bound -> next lower bound
                frame_id += 1
                timestamp_list[str(frame_id)] = timestamp_lower_bound
                points_by_timestamp[str(frame_id)] = []
            points_by_timestamp[str(frame_id)].append([x, y, z])
            
    return points_by_timestamp

#save each frames to pcd file
def save_points(points_by_timestamp, output_dir,res=10):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Find the biggest timestamp
    biggest_frame_id = max(points_by_timestamp.keys(), key=float)
    smallest_frame_id = min(points_by_timestamp.keys(), key=float)
    
    # Iterate through the accumulated points and create PCD files
    for frame_id, points in points_by_timestamp.items():
        
        # Create an Open3D point cloud
        point_cloud = o3d.geometry.PointCloud()
        point_cloud.points = o3d.utility.Vector3dVector(points)

        # Save the point cloud to a PCD file with the timestamp as the filename
        output_file = f'{output_dir}/{"{:05}".format(int(frame_id)*res)}.pcd'
        o3d.io.write_point_cloud(output_file, point_cloud)

        print(f"{frame_id}/{biggest_frame_id}")
    
def make_save_dir_path(data_path, 
                       data_type_name="LIVOX_Hallway_pcds", 
                       file_name="jogging_fast_4th", 
                       res=10, start=0):
    dir_name = rf"res{res}ms_" + rf"start{start}s" #res10ms_start25s
    return os.path.join(data_path, data_type_name, file_name, dir_name)
        

def main():
    
    res = 10 #time resolution of frames(mili second)
    start = 13.5 #the time(second) to set as frame0 <- this should be the time human started to run.
    
    data_type_name_csv = "LIVOX_Hallway_csv"
    data_type_name_pcd = "LIVOX_Hallway_pcds"
    file_name="jogging_fast_4th"
    
    # Replace 'your_input.csv' and 'output_directory' with your actual input CSV file and output directory
    csv_file_path = os.path.join(DATA_PATH, data_type_name_csv, file_name+".csv")
    output_dir = make_save_dir_path(data_path=DATA_PATH, 
                       data_type_name=data_type_name_pcd, 
                       file_name=file_name, 
                       res=res, start=start)

    print("making points list")
    points_by_timestamp = read_csv(csv_file_path, res, start)
    print("points list is made")  
    
    save_points(points_by_timestamp, output_dir, res)
    print("Done!")
    
if __name__ == "__main__":
    main()