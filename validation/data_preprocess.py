from scipy.interpolate import interp1d
import numpy as np
import pandas as pd

def cs_interpolate(chunk):
    interpolator = interp1d(chunk['Time'], chunk['Velocity'], kind='cubic')
    t_new = np.linspace(chunk['Time'].min(), chunk['Velocity'].max(), 1)
    v_new = abs(interpolator(t_new))
    gt_interp = pd.DataFrame({'Time': t_new, 'Velocity': v_new})
    
    return gt_interp