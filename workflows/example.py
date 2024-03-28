import flytekit
from flytekit import task, workflow
from flytekit.types.directory import FlyteDirectory
from pathlib import Path
import os
import subprocess


@task()
def preprocess_data(raw_data_dir: FlyteDirectory) -> FlyteDirectory:
    """Takes in a raw dataset and returns a preprocessed dataset."""
    print(f"Preprocessing data in {raw_data_dir}")

    # get the working directory of the current execution
    # https://docs.flyte.org/en/latest/api/flytekit/generated/flytekit.ExecutionParameters.html#flytekit-executionparameters
    print(f"Working directory: {flytekit.current_context().working_directory}")
    working_dir = flytekit.current_context().working_directory

    # FlyteDirectory subclasses os.PathLike (I think) and I guess that's why this is
    # possible to use os.path functions with it but I've also seen examples of accessing
    # the attributes
    # https://docs.flyte.org/en/latest/_modules/flytekit/types/directory/types.html#FlyteDirectory
    local_dir = Path(os.path.join(working_dir, "preprocessed_data"))
    local_dir.mkdir(exist_ok=True)
    print(f"Local directory: {local_dir}")

    # Use the nerfstudio command for preprocessing data
    # This is the command that I need to execute
    # ns-process-data record3d --data 2024-03-17--18-25-12/EXR_RGBD --output-dir my-data
    print(f"Preprocessing data in {raw_data_dir}")
    command = f"ns-process-data record3d --data {raw_data_dir} --output-dir {local_dir}"
    subprocess.run(command, shell=True)

    return FlyteDirectory(path=f"{local_dir}")


@workflow
def wf(dir: FlyteDirectory) -> FlyteDirectory:
    # I'm going to try to use this to pass in strings to a directory and see what
    # happens
    return preprocess_data(raw_data_dir=dir)


if __name__ == "__main__":
    # Execute the workflow by invoking it like a function and passing in
    # the necessary parameters
    print(f"Running wf() {wf(dir='2024-03-17--18-25-12/EXR_RGBD')}")
