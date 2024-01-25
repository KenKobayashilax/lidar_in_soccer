# LiDAR in Soccer Processing Team
This reppository is for processig point clouds data of LiDAR in soccer.  
## Data structure
Please edit `config.ini` file and change __DATA_PATH__ and __BASE_PATH__ to yours.  
Data structure under __DATA_PATH__ is as follows.
<pre>
DATA_PATH
├─LIVOX_Hallway
|  └─jogging_fast_4th.lvx
├─LIVOX_Hallway_csv
|  └─jogging_fast_4th.csv
├─LIVOX_Hallway_pcds
│  └─jogging_fast_4th
│      └─res10ms
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

use `csv2pcd.ipynb` or run `get_frames/csv2pcd.py`

## Clustrization
## Human detection
## Compute CoM(center of mass)
## Evaluation
