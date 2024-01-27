# LiDAR in Soccer Processing Team
This reppository is for processig point clouds data of LiDAR in soccer.  
## Data structure
Please edit `settings.py` file and change __DATA_PATH__ and __BASE_PATH__ to yours.  
Data structure under __DATA_PATH__ is as follows.
<pre>
DATA_PATH
├─LIVOX_Hallway
|  └─jogging_fast_4th.lvx
├─LIVOX_Hallway_csv
|  └─jogging_fast_4th.csv
├─LIVOX_Hallway_pcds
│  └─jogging_fast_4th
│      └─res10ms_start13.5s
├─New_data
│  └─New_data
│      └─pcds
└─recorded data
    └─recorded data
</pre>
We first focus on `jogging_fast_4th.lvx` data.
## Get frames from csv data  
At first, get `jogging_fast_4th.csv` file from livox viewer(use `Tools > File Convertor > lvx to csv`).  

**input: csv file  
output: sequence of pcd files**  
You can change time resolution per frame and timing of frame0 by using `res` and `start` arguement.  
Use `csv2pcd.ipynb` or run `get_frames/csv2pcd.py`  

## Clustrization  
**input: raw pcd files  
output: clusterized labels**  
By using `check_clusterization.ipynb`, you can clusterize point clouds and visualize the clusters.  

At the first cell, you can process sequential pcd files, and second, single pcd file.
At the first cell, you firstly select the viewpoint and close the window. After that, you can see the clusters from the selected viewpoint.  
You can process single pcd files also by the `clusterization/clusterize.py`, but not sequential data.  

In both cells, you can change data_path. And, at the `clusterize.clusterize` function, you can define more arguments than written in .ipynb file. So, please take a look at `clusterization/clusterize.py`.

## Human detection
## Compute CoM(center of mass)
## Evaluation
