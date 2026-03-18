import pandas as pd
import numpy as np

def create_gear_matrix(df):
    gear_df=df
    # Define RPM bins and labels
    spd_bins = list(range(-25, 1426, 50))
    spd_labels = list(range(0, 1401, 50))
    # Example
    # bins	labels
    # -25	    0   -> [-25, 25)
    # 25	    50   -> [25, 75)
    # 75	    100   -> [75, 125)
    # 125	    150   -> [125, 175)
    # 175	    200   -> [175, 225)

    
    # Define Torque bins and labels 
    torque_bins = list(range(-325, 726, 50))
    torque_labels = list(range(-300, 701, 50))
    gear_df['spd_Band'] = pd.cut(gear_df['Spd'], bins=spd_bins, labels=spd_labels, right=False)   # change name of column to "op_spd_band"
    gear_df['Torque_Band'] = pd.cut(gear_df['Trq'], bins=torque_bins, labels=torque_labels, right=False)
    
    # Drop rows with missing band info
    gear_df = gear_df.dropna(subset=['spd_Band', 'Torque_Band'])
    
    # Group and sum mileage
    grouped = gear_df.groupby(['Torque_Band', 'spd_Band'])['Mileage'].sum().reset_index()
    
    # Pivot to form the matrix
    matrix = grouped.pivot(index='Torque_Band', columns='spd_Band', values='Mileage').fillna(0).round(2)
    matrix=matrix.to_numpy()[::-1]
    columns=spd_labels
    indexes=torque_labels[::-1]

    gear_mat={}
    mileage_values = np.where(matrix == 0, 0, matrix)
    mileage_percentages = np.where(matrix == 0, 0, matrix / matrix.sum())

    gear_mat['Mileage_values']=mileage_values
    gear_mat['Mileage_percentages']=mileage_percentages
    # print(type(gear_mat['Mileage_percentages']))
    return gear_mat