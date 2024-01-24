import pcl
import numpy as np
import laspy
import open3d as o3d


# 指定 LAS 文件路径
las_file_path = fr"C:/Users/15kob/Documents/study/abroad/lectures/LiDAR_in_soccer/data/New_data/New_data/27.las"

# 使用 laspy 打开 LAS 文件
las_file = laspy.read(las_file_path)



# 获取 LAS 文件中的点云数据
point_cloud_data = np.vstack([las_file.x, las_file.y, las_file.z]).T

# 创建 Open3D 点云对象
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(point_cloud_data)

# 保存为 PCD 文件
o3d.io.write_point_cloud(fr"C:/Users/15kob/Documents/study/abroad/lectures/LiDAR_in_soccer/data/New_data/New_data/27.pcd", pcd)