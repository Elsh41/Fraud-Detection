import pandas as pd
import numpy as np
import socket
import struct

def ip_to_int(ip):
    """Convert an IPv4 string address to an integer format."""
    try:
        if pd.isna(ip) or not isinstance(ip, str):
            return np.nan
        return struct.unpack("!I", socket.inet_aton(ip.strip()))[0]
    except Exception:
        return np.nan

def merge_ip_range(fraud_df, ip_df):
    """
    Perform a range-based merge between Fraud Data and IP-to-Country Data.
    Optimized via sorting and merge_asof to handle large datasets efficiently.
    """
    # Ensure columns are sorted for merge_asof
    fraud_df = fraud_df.sort_values('ip_address_int')
    ip_df = ip_df.sort_values('lower_bound_ip_address')
    
    # Merge on the closest lower bound
    merged = pd.merge_asof(
        fraud_df, 
        ip_df, 
        left_on='ip_address_int', 
        right_on='lower_bound_ip_address', 
        direction='backward'
    )
    
    # Filter out entries where ip_address_int exceeds the upper bound
    valid_mask = merged['ip_address_int'] <= merged['upper_bound_ip_address']
    merged.loc[~valid_mask, 'country'] = 'Unknown'
    
    return merged