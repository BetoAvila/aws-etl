import pandas as pd
import numpy as np


def lambda_handler(event, context):
    data_url = "https://raw.githubusercontent.com/BetoAvila/datasets/main/random_datasets/ds_1.csv"
    bucket_name = "etl_bucket"
    filename = "etl_output.parquet"
    dest_URI = f"s3://{bucket_name}/target_files/"

    # Data engineering
    df = pd.read_csv(data_url)
    df = df.astype({
        "id": str,
        "class": str,
        "memory": np.int16,
        "percentage": np.float16,
        "ratio": np.float16,
        "fob": str,
        "dp": str,
        "recovered": np.int8,
    })

    df = (df.groupby(["dp"]).agg({
        "memory": ["min", "max", "count"],
        "percentage": ["max", "mean"],
        "ratio": "max",
    }).reset_index())

    # There are probably better ways to flatten multi index df
    df = pd.DataFrame({
        "dp": df.dp,
        "memory_min": df["memory", "min"],
        "memory_max": df["memory", "max"],
        "memory_count": df["memory", "count"],
        "percentage_max": df["percentage", "max"],
        "percentage_avg": df["percentage", "mean"],
        "ratio_max": df["ratio", "max"],
    })

    # Save aggregated df into S3 bucket as parquet file
    try:
        df.to_parquet(dest_URI + filename, index=False)
    except Exception as e:
        print(f"Error on bucket data load:\n{e}")
        raise e
    print(df.head())
