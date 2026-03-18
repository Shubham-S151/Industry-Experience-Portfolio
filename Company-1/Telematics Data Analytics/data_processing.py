from vehicle_telematics_codes_with_temp.data_import import get_files_paths,combine_files
from vehicle_telematics_codes_with_temp.config import Root_path,Coeff_path

import numpy as np
import pandas as pd

t2_value = 138

def get_gear_ratios(path,vid,gear):
    veh_df=pd.read_csv(path)
    fltr=veh_df[gear][veh_df['ID']==vid]
    fltr_1 = veh_df.loc[veh_df['ID'] == vid, ['Model', 'TRANSMISSION_TYPE']]
    if fltr_1.empty:
        raise ValueError(f"No record found for ID={vid}")

    # Combine Model and TRANSMISSION_TYPE into one string
    model_transmission = f"{fltr_1.iloc[0]['Model']} {fltr_1.iloc[0]['TRANSMISSION_TYPE']}"
    print(model_transmission)  # Output: YXA 6A
    return fltr.to_list()[0],model_transmission

def get_radius(path,vid):
    veh_df=pd.read_csv(path)
    fltr=veh_df[veh_df['ID']==vid]
    return float(fltr['Tire Radius_x'].values)
    
def process_data(Root_path,vid,Coeff_path):
    files = get_files_paths(Root_path)
    print('Paths extracted successfully')
    df = combine_files(files)
    print('Data combined successfully')
    if df is not None:
        print(f"{'#'*30}|   Completed Data Import   |{'#'*30}")
    df = remove_null(df)
    print('Null values removed successfully')
    df = change_dtype(df)
    print('Data type changed successfully')
    df = create_features(df,vid,Coeff_path)
    print('Features created successfully')
    model_transmission=get_gear_ratios(Coeff_path,vid,'GR_1')[1]
    if df is not None:
        print(f"{'#'*30}|   Completed Data Cleaning   |{'#'*30}")
    return df,model_transmission
    
files = get_files_paths(Root_path)
df = combine_files(files)

def remove_null(df):
    try:
        df = df.sort_values(by=['GPS_TimeStamp_Local', 'msec']).dropna()
        print('Null values removed an values sorted successfully')
        return df
    except:
        print('Values sorted failed')

def change_dtype(df):
    try:
        df = df.astype({
        'msec': int,
        'AcclActPos': float,
        'EgSpd': float,
        'EgTrqAct': float,
        'OsideAirTmp': float,
        'TMActGear' : int,
        'TMActGearRatio': float,
        'TMOilTmp': float,
        'VhclSpd' : float
    })
        return df
    except Exception as e:
        print(f'Error: {e}')

def create_features(df,vid,Coeff_path):
    try :
        df=df.loc[(df['TMActGear']>0)&(df['TMActGear']<7)].copy()

        df['Time'] = [round(0.1*i,1) for i in range(len(df))]
        df['Step_sec'] = df['msec'].diff().fillna(0)
        # Make sure 'Step_sec' is non-negative by adding 1000 if negative
        df['Step_sec'] = np.where(df['Step_sec'] < 0, (df['Step_sec'] + 1000), df['Step_sec'])

        # Convert 'Step_sec' from milliseconds to seconds
        df['Step_sec'] = df['Step_sec'] / 1000

        df['Target_Torque_Nm'] =  np.where(df['TMActGear'] == 1, 0.7*t2_value, 
                                    np.where(df['TMActGear'] == 8, 0.5*t2_value,t2_value))
        # Mileage in km = [VhclSpd in km/h * Step_sec in seconds] / 3600
        df['Mileage_km'] = (df['VhclSpd'] * df['Step_sec']) / 3600  
        # Total Engine Revolution in each step = [Engine Speed in rpm * Step_sec in seconds] / 60

        df['Total_Eng_Rev'] = (df['EgSpd'] * df['Step_sec']) / 60         # in round per second
        # N2 = N1 * (T1/T2)^n
        # @ power 3.3

        # Calculate the ratio and raise it to the power of 3.3
        ratio_power = np.where(df['EgTrqAct'] > 0, (df['EgTrqAct'] / df['Target_Torque_Nm']) ** 3.3, 0)

        # Multiply by Total_Eng_Rev where EgTrqAct > 0
        df['Est_Eng_Rev_3.3'] = ratio_power * df['Total_Eng_Rev']
        # N2 = N1 * (T1/T2)^n 
        # @ power 5

        # Calculate the ratio and raise it to the power of 5
        ratio_power = np.where(df['EgTrqAct'] > 0, (df['EgTrqAct'] / df['Target_Torque_Nm']) ** 5, 0)

        # Multiply by Total_Eng_Rev where EgTrqAct > 0
        df['Est_Eng_Rev_5'] = ratio_power * df['Total_Eng_Rev']
        # N2 = N1 * (T1/T2)^n
        # @ power 11

        # Calculate the ratio and raise it to the power of 11
        ratio_power = np.where(df['EgTrqAct'] > 0, (df['EgTrqAct'] / df['Target_Torque_Nm']) ** 11, 0)

        # Multiply by Total_Eng_Rev where EgTrqAct > 0
        df['Est_Eng_Rev_11'] = ratio_power * df['Total_Eng_Rev']
        
        # Creating Output Torque column
        conditions = [
        df['TMActGear'] == 1,
        df['TMActGear'] == 2,
        df['TMActGear'] == 3,
        df['TMActGear'] == 4,
        df['TMActGear'] == 5,
        df['TMActGear'] == 6]

        ratios = [get_gear_ratios(Coeff_path, vid, f'GR_{i}')[0] for i in range(1, 7)]
        radius = [get_radius(Coeff_path, vid) for i in range(1, 7)]

        df['OpTrq'] = np.select(conditions, [df['EgTrqAct'] * r for r in ratios], default=df['EgTrqAct'])
        df['OpSpd'] = np.select(conditions, [df['VhclSpd']*1000 / 120*3.1416*r for r in radius], default=0)
        return df
    except Exception as e:
        print(f'Error: {e}')