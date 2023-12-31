import mlflow
import time

# To set up Databricks CE authentication, we can use the API mlflow.login(), which will prompt you for required information:
# Databricks Host: Use https://community.cloud.databricks.com/
# Username: Your email address that signs in Databricks CE.
# Password: Your password of Databricks CE.
mlflow.login()

mlflow.set_tracking_uri("databricks")
mlflow.set_experiment("/check-databricks-connection")

with mlflow.start_run() as run:
    mlflow.log_metric("foo", 1)
    mlflow.log_metric("bar", 2)
    time.sleep(15)

print(mlflow.MlflowClient().get_run(run.info.run_id).data)
