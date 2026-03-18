from vehicle_telematics_codes.data_import import get_files_paths, combine_files
from vehicle_telematics_codes.config import Root_path

from pyspark.sql.functions import col, when, lit, pow, lag, monotonically_increasing_id
from pyspark.sql.window import Window

t2_value = 138

def process_data(root_path):
    files = get_files_paths(root_path)
    print("Paths extracted successfully")
    
    df = combine_files(files)
    print("Data combined successfully")
    
    df = remove_null(df)
    print("Null values removed successfully")
    
    df = change_dtype(df)
    print("Data type changed successfully")
    
    df = create_features(df)
    print("Features created successfully")
    
    df=spark_to_pd(df)
    print('Data Loaded to Pandas')
    
    return df

def remove_null(df):
    return df.dropna().orderBy("GPS_TimeStamp_Local", "msec")

def change_dtype(df):
    return df.select(
        col("msec").cast("int"),
        col("AcclActPos").cast("float"),
        col("EgSpd").cast("float"),
        col("EgTrqAct").cast("float"),
        col("OsideAirTmp").cast("float"),
        col("TMActGear").cast("int"),
        col("TMActGearRatio").cast("float"),
        col("TMOilTmp").cast("float"),
        col("VhclSpd").cast("float"),
        col("GPS_TimeStamp_Local")
    )

def create_features(df):
    # Add row index for Time column
    df = df.withColumn("row_id", monotonically_increasing_id())
    df = df.withColumn("Time", (col("row_id") * 0.1).cast("double"))

    # Calculate Step_sec using lag
    window_spec = Window.orderBy("GPS_TimeStamp_Local", "msec")
    df = df.withColumn("prev_msec", lag("msec").over(window_spec))
    df = df.withColumn("Step_sec_raw", col("msec") - col("prev_msec"))
    df = df.withColumn("Step_sec", when(col("Step_sec_raw") < 0, col("Step_sec_raw") + 1000).otherwise(col("Step_sec_raw")) / 1000)

    # Target Torque
    df = df.withColumn("Target_Torque_Nm", when(col("TMActGear") == 1, 0.7 * t2_value)
                                        .when(col("TMActGear") == 8, 0.5 * t2_value)
                                        .otherwise(t2_value))

    # Mileage and Engine Revolutions
    df = df.withColumn("Mileage_km", (col("VhclSpd") * col("Step_sec")) / 3600)
    df = df.withColumn("Total_Eng_Rev", (col("EgSpd") * col("Step_sec")) / 60)

    # Est_Eng_Rev with powers 3.3, 5, 11
    for power in [3.3, 5, 11]:
        ratio = (col("EgTrqAct") / col("Target_Torque_Nm"))
        ratio_power = when(col("EgTrqAct") > 0, pow(ratio, power)).otherwise(0)
        df = df.withColumn(f"Est_Eng_Rev_{power}", ratio_power * col("Total_Eng_Rev"))

    return df

def spark_to_pd(spark_df):
    pandas_df = spark_df.toPandas()
    return pandas_df