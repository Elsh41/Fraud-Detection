import pandas as pd
import numpy as np
import socket
import struct
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_data(file_path):
    """Safely loads CSV data with error handling."""
    try:
        df = pd.read_csv(file_path)
        logging.info(f"Successfully loaded {file_path} with shape {df.shape}")
        return df
    except FileNotFoundError as e:
        logging.error(f"File not found at {file_path}: {str(e)}")
        raise e
    except Exception as e:
        logging.error(f"Error loading file {file_path}: {str(e)}")
        raise e

def ip_to_int(ip):
    """Converts IPv4 string address to integer format."""
    try:
        if pd.isna(ip) or not isinstance(ip, (str, float, int)):
            return np.nan
        if isinstance(ip, (int, float)) or (isinstance(ip, str) and ip.strip().replace('.','').isdigit()):
            return int(float(ip))
        return struct.unpack("!I", socket.inet_aton(ip.strip()))[0]
    except Exception:
        return np.nan

def merge_ip_range(fraud_df, ip_df):
    """
    Performs range-based merge between Fraud Data and IP-to-Country Data.
    Uses merge_asof with aligned data types to avoid MergeErrors.
    """
    try:
        # 1. Create local copies to avoid modifying original DataFrames in-place
        fraud_temp = fraud_df.copy()
        ip_temp = ip_df.copy()
        
        # 2. Force matching types (float64 is safest for handling both integer and float-based IP representations)
        fraud_temp['ip_address_int'] = fraud_temp['ip_address_int'].astype(float)
        ip_temp['lower_bound_ip_address'] = ip_temp['lower_bound_ip_address'].astype(float)
        ip_temp['upper_bound_ip_address'] = ip_temp['upper_bound_ip_address'].astype(float)
        
        # 3. Sort values (strictly required by pd.merge_asof)
        fraud_sorted = fraud_temp.sort_values('ip_address_int')
        ip_sorted = ip_temp.sort_values('lower_bound_ip_address')
        
        # 4. Perform the asof merge
        merged = pd.merge_asof(
            fraud_sorted, 
            ip_sorted, 
            left_on='ip_address_int', 
            right_on='lower_bound_ip_address', 
            direction='backward'
        )
        
        # 5. Invalidate rows where the user's IP exceeds the upper range bound
        valid_mask = merged['ip_address_int'] <= merged['upper_bound_ip_address']
        merged.loc[~valid_mask, 'country'] = 'Unknown'
        merged['country'] = merged['country'].fillna('Unknown')
        
        logging.info("Range-based IP lookup complete successfully with matching float64 types.")
        return merged
    except Exception as e:
        logging.error(f"Error during range-based IP merge: {str(e)}")
        raise e