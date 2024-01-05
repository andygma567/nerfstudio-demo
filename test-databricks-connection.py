import re
import mlflow
import time
import subprocess
import argparse
import psutil

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--data-path", help="Path to the video data file")
parser.add_argument("--processed-data-dir", help="Path to the processed data directory")
args = parser.parse_args()

# Set the global variables based on the command line arguments
DATA_PATH = args.data_path if args.data_path else "/path/to/video.mp4"
PROCESSED_DATA_DIR = args.processed_data_dir if args.processed_data_dir else "/path/to/processed/data"

# To set up Databricks CE authentication, we can use the API mlflow.login(), 
# which will prompt you for required information:
# Databricks Host: Use https://community.cloud.databricks.com/
# Username: Your email address that signs in Databricks CE.
# Password: Your password of Databricks CE.
mlflow.login()

mlflow.set_tracking_uri("databricks")
mlflow.set_experiment("/check-databricks-connection")
mlflow.enable_system_metrics_logging()

with mlflow.start_run() as run:
    # Check CPU cores
    cpu_cores = psutil.cpu_count()
    mlflow.log_param("cpu_cores", cpu_cores)
    
    # Check total available RAM
    ram_info = psutil.virtual_memory()
    mlflow.log_param("ram_total", ram_info.total)
    mlflow.log_param("ram_available", ram_info.available)

    # Check GPU
    try:
        gpu_info_output = subprocess.check_output("nvidia-smi", shell=True).decode('utf-8')
        mlflow.log_param("gpu_info", gpu_info_output.strip())
    except subprocess.CalledProcessError:
        mlflow.log_param("gpu_info", "nvidia-smi command not found or no NVIDIA GPU detected")

    # execute the preprocessing and training steps
    preprocess_start_time = time.time()
    subprocess.run(["ns-process-data", "video", "--data", DATA_PATH, "--output-dir", PROCESSED_DATA_DIR])
    preprocess_end_time = time.time()
    preprocessing_time = preprocess_end_time - preprocess_start_time
    print(f"Execution time: {preprocessing_time} seconds")
    
    mlflow.log_metric("preprocessing_time", preprocessing_time)
    mlflow.log_artifact(PROCESSED_DATA_DIR)

    start_time = time.time()
    subprocess.run(["ns-train", "nerfacto", "--data", PROCESSED_DATA_DIR])
    end_time = time.time()
    execution_time = end_time - start_time
    
    mlflow.log_metric("training_time", execution_time)
    OUTPUTS_DIR = PROCESSED_DATA_DIR + "/outputs/"
    mlflow.log_artifact(OUTPUTS_DIR)

print(mlflow.MlflowClient().get_run(run.info.run_id).data)
