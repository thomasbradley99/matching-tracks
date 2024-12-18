import pandas as pd
import numpy as np
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean

def extract_features(data):
    """Extract features for alignment."""
    return data[["pitch_x", "pitch_y"]].values

def calculate_dtw_offset(left_data, right_data):
    """Calculate time offset using Dynamic Time Warping."""
    left_features = extract_features(left_data)
    right_features = extract_features(right_data)
    
    distance, path = fastdtw(left_features, right_features, dist=euclidean)
    offsets = [p[0] - p[1] for p in path]
    return np.median(offsets)

if __name__ == "__main__":
    left_data = pd.read_csv("path/to/camL_1.csv")
    right_data = pd.read_csv("path/to/camR_1.csv")

    # Calculate DTW offset
    dtw_offset = calculate_dtw_offset(left_data, right_data)
    print(f"DTW Offset: {dtw_offset} frames")
