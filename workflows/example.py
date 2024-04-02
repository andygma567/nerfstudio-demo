import flytekit
from flytekit import task, workflow
from flytekit.types.directory import FlyteDirectory
from pathlib import Path
import os
import subprocess
import re
import pty


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


@task()
def send_data(preprocessed_data: FlyteDirectory) -> str:
    """Sends the preprocessed data somewhere and returns a string."""
    # I need to use pty.openpty() to open a pseudo-terminal I previously tried to use
    # subprocess.Popen() with stdout=subprocess.PIPE, but it didn't work I think it has
    # to do with the fact that the command runpodctl send my-data is not writing to
    # stdout and so I can't read it line by line using subprocess.stdout.readline()
    main, secondary = pty.openpty()  # Open a pseudo-terminal
    command = f"runpodctl send {preprocessed_data}"
    process = subprocess.Popen(
        command, stdout=secondary, stderr=subprocess.STDOUT, shell=True
    )
    os.close(
        secondary
    )  # Close the secondary to ensure we're only communicating via the main

    output = ""
    while True:
        try:
            # Reading from the main gives us the subprocess's output
            data = os.read(main, 1024).decode("utf-8")
            output += data
            print(data, end="")  # Print the subprocess output in real-time
            if "On the other computer run" in output:
                # Once we have the specific line, we can break out of the loop
                break
        except OSError:
            # This can happen if the subprocess closes its output, or we forcibly close
            # the main
            break

    process.kill()  # Ensure the subprocess is terminated

    # Attempt to extract the runpodctl receive command
    receive_command_match = re.search(r"(runpodctl receive [0-9a-z-]+)", output)
    output = receive_command_match.group(1)
    print(f"Output: {output}")
    return output


@workflow
def wf(dir: FlyteDirectory) -> FlyteDirectory:
    # I'm going to try to use this to pass in strings to a directory and see what
    # happens
    return preprocess_data(raw_data_dir=dir)


if __name__ == "__main__":
    # Execute the workflow by invoking it like a function and passing in
    # the necessary parameters
    print(f"Running wf() {wf(dir='2024-03-17--18-25-12/EXR_RGBD')}")
