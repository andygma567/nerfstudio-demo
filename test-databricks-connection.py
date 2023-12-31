import mlflow
import time

mlflow.login()

mlflow.set_tracking_uri("databricks")
mlflow.set_experiment("/check-databricks-connection")

with mlflow.start_run() as run:
    mlflow.log_metric("foo", 1)
    mlflow.log_metric("bar", 2)
    time.sleep(15)

print(mlflow.MlflowClient().get_run(run.info.run_id).data)
