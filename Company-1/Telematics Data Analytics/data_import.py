import os 
import pandas as pd

def get_files_paths(path):
    paths=[]
    try :
        for i in os.listdir(path):
            if os.path.isdir(i):
                for file in os.listdir(i):
                    if get_type(i)=='parquet':
                        paths.append(os.path.join(path,i,file))
            else :
                if get_type(i)=='parquet':
                    paths.append(os.path.join(path,i))
        return paths
    except Exception as e:
        print(e)

# def combine_files(spark,paths):
#     spark_df = spark.read.parquet(
#     *paths)
#     return spark_df

def combine_files(paths):
    df_list=[]
    try:
        for path in paths:
            curr_df = pd.read_parquet(path, engine='fastparquet')
            df_list.append(curr_df)    
        all_df = pd.concat(df_list)
        return all_df
    except Exception as e:
        print(e)

def get_type(path): 
        return path.split('.')[-1]
    