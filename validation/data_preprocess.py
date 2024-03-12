from scipy.interpolate import interp1d
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter
from sklearn.metrics import mean_squared_error


# CubicSpline Interpolation
def cs_interpolate(chunk, filter):
    if filter == False:
        interpolator = interp1d(chunk['Time'], chunk['Velocity'], kind='cubic')
        t_new = np.linspace(chunk['Time'].min(), chunk['Velocity'].max(), 1)
        v_new = abs(interpolator(t_new))
        gt_interp = pd.DataFrame({'Time': t_new, 'Velocity': v_new})
    else:
        interpolator = interp1d(chunk['Time'], chunk['Filtered_Velocity'], kind='cubic')
        t_new = np.linspace(chunk['Time'].min(), chunk['Filtered_Velocity'].max(), 1)
        v_new = abs(interpolator(t_new))
        gt_interp = pd.DataFrame({'Time': t_new, 'Filtered_Velocity': v_new})
    
    return gt_interp


# the lowpass filter
def butter_lowpass_filter(data, cutoff_freq, sample_rate, order=4):
    nyquist = 0.5 * sample_rate
    normal_cutoff = cutoff_freq / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = lfilter(b, a, data)
    
    return y


# perform interpolation
def apply_interp_to_gt(gt, gt_interp_path, chunk_size, filter):
    if filter == False:
        gt_new = pd.DataFrame(columns=['Time', 'Velocity'])
    else:
        gt_new = pd.DataFrame(columns=['Time', 'Filtered_Velocity'])

    num_chunks = len(gt) // chunk_size

    for i in range(num_chunks):
        chunk = gt.iloc[i * chunk_size:(i + 1) * chunk_size]
        gt_interp = cs_interpolate(chunk, filter)
        gt_new = pd.concat([gt_new, gt_interp], ignore_index=True)

    gt_new.to_csv(gt_interp_path, index=False)

    return(gt_new)


# alignment
def align_dataframe(gt_new, ms, len_diff, filter):
    min_rmse = np.inf
    best_offset = 0

    if len_diff > 0:
        df1 = ms
        df2 = gt_new
    else:
        df1 = gt_new
        df2 = ms

    # calculate the RMSE at different offsets
    for offset in range(abs(len_diff) + 1):
        offset_df2 = df2.copy()
        index_list = np.arange(offset, offset + len(df1))
        
        if filter == False:
            rmse = np.sqrt(
                mean_squared_error(
                    offset_df2.iloc[np.min(index_list):np.max(index_list)+1]['Velocity'], df1['Velocity'].values
                    )
                )
        else:
            rmse = np.sqrt(
            mean_squared_error(
                offset_df2.iloc[np.min(index_list):np.max(index_list)+1]['Filtered_Velocity'], df1['Filtered_Velocity'].values
                )
            )

        # Update minimum error and offset
        if rmse < min_rmse:
            min_rmse = rmse
            best_offset = offset
            best_df2 = offset_df2.iloc[np.min(index_list):np.max(index_list)+1]
    
    return min_rmse, best_df2, best_offset


# plot
def plot_validation_result(len_diff, best_chunk, gt_new, ms):
    if isinstance(best_chunk, float):
        print("Error: Alignment unsuccessful. Please check your data and alignment parameters.")
        return

    if len_diff > 0:
        aligned_gt = best_chunk
        time_offset = aligned_gt.index[0] - gt_new.index[0]
        plt.plot(aligned_gt.index, aligned_gt['Velocity'], label='Ground Truth', color='blue')
        plt.plot(ms.index + time_offset, ms['Velocity'], label='LiDAR_Measurement', color='red')
    else:
        aligned_ms = best_chunk
        time_offset = aligned_ms.index[0] - ms.index[0]
        plt.plot(gt_new.index + time_offset, gt_new['Velocity'], label='Ground Truth', color='blue')
        plt.plot(aligned_ms.index, aligned_ms['Velocity'], label='LiDAR_Measurement', color='red')
    
    plt.legend()
    plt.xlabel('Time')
    plt.ylabel('Velocity')
    plt.title('Validation')
    plt.tight_layout()
    plt.show()



def plot_validation_filtered_result(len_diff_f, best_chunk_f, gt_f_new, ms):
    if len_diff_f > 0:
        aligned_gt_f = best_chunk_f
        time_offset_f = aligned_gt_f.index[0] - gt_f_new.index[0]
        plt.plot(aligned_gt_f.index, aligned_gt_f['Filtered_Velocity'], label='Ground Truth',color='blue')
        plt.plot(ms.index + time_offset_f, ms['Filtered_Velocity'], label='LiDAR_Measurement', color='red')
    else:
        aligned_ms_f = best_chunk_f
        time_offset_f = aligned_ms_f.index[0] - ms.index[0]
        plt.plot(gt_f_new.index + time_offset_f, gt_f_new['Filtered_Velocity'], label='Ground Truth',color='blue')
        plt.plot(aligned_ms_f.index , aligned_ms_f['Filtered_Velocity'], label='LiDAR_Measurement', color='red')
    plt.legend()

    plt.xlabel('Time')
    plt.ylabel('Filtered_Velocity')
    plt.title('Validation_filtered')

    plt.tight_layout()
    plt.show()
