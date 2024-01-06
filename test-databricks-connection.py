import mlflow
import time
import subprocess
import argparse
import psutil

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument(
    "--data-path", help="Path to the video data file", default="~/video.mp4"
)
# Sometimes I need to run the terminal command directly before this will work. I don't know why.
parser.add_argument(
    "--processed-data-dir",
    help="Path to the processed data directory",
    default=".",
)
parser.add_argument(
    "--num-frames-target",
    help="Target number of frames to use per video",
    type=int,
    default=300,
)
parser.add_argument(
    "--max-num-iterations",
    help="Maximum number of iterations",
    type=int,
    default=30000,
)
args = parser.parse_args()

# Set the global variables based on the command line arguments
DATA_PATH = args.data_path
PROCESSED_DATA_DIR = args.processed_data_dir
NUM_FRAMES_TARGET = args.num_frames_target
MAX_NUM_ITERATIONS = args.max_num_iterations

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
    total_ram_gb = ram_info.total / (1024**3)
    mlflow.log_param("ram_total (in GB)", total_ram_gb)

    # Check GPU
    try:
        gpu_info_output = subprocess.check_output("nvidia-smi", shell=True).decode(
            "utf-8"
        )
        mlflow.log_param("gpu_info", gpu_info_output.strip())
    except subprocess.CalledProcessError:
        mlflow.log_param(
            "gpu_info", "nvidia-smi command not found or no NVIDIA GPU detected"
        )

    mlflow.set_tag("Dataset", DATA_PATH)
    mlflow.log_param("num_frames_target", NUM_FRAMES_TARGET)

    # execute the preprocessing and training steps
    preprocess_start_time = time.time()
    subprocess.run(
        [
            "ns-process-data",
            "video",
            "--data",
            DATA_PATH,
            "--output-dir",
            PROCESSED_DATA_DIR,
            "--num-frames-target",
            str(NUM_FRAMES_TARGET),
            "--matching-method",
            "sequential",
        ]
    )
    preprocess_end_time = time.time()
    preprocessing_time = preprocess_end_time - preprocess_start_time
    print(f"Execution time: {preprocessing_time} seconds")

    mlflow.log_metric("preprocessing_time", preprocessing_time)

    mlflow.log_param("max-num-iterations", MAX_NUM_ITERATIONS)
    start_time = time.time()
    subprocess.run(
        [
            "ns-train",
            "nerfacto",
            "--data",
            PROCESSED_DATA_DIR,
            "--vis",
            "tensorboard",
            # Using the default viewer prevents the script from continuing
            "--max-num-iterations",
            str(MAX_NUM_ITERATIONS),
        ]
    )
    end_time = time.time()
    execution_time = end_time - start_time

    mlflow.log_metric("training_time", execution_time)
    OUTPUTS_DIR = PROCESSED_DATA_DIR + "/outputs/"

print(mlflow.MlflowClient().get_run(run.info.run_id).data)
