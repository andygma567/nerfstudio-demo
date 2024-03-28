import os
import pty
import subprocess
import re


def run_command_and_capture_output(command):

    # I need to use pty.openpty() to open a pseudo-terminal I previously tried to use
    # subprocess.Popen() with stdout=subprocess.PIPE, but it didn't work I think it has
    # to do with the fact that the command runpodctl send my-data is not writing to
    # stdout and so I can't read it line by line using subprocess.stdout.readline()
    main, secondary = pty.openpty()  # Open a pseudo-terminal
    process = subprocess.Popen(
        command, stdout=secondary, stderr=subprocess.STDOUT, shell=True
    )
    os.close(
        secondary
    )  # Close the slave to ensure we're only communicating via the master

    output = ""
    while True:
        try:
            # Reading from the master gives us the subprocess's output
            data = os.read(main, 1024).decode("utf-8")
            output += data
            print(data, end="")  # Print the subprocess output in real-time
            if "On the other computer run" in output:
                # Once we have the specific line, we can break out of the loop
                break
        except OSError:
            # This can happen if the subprocess closes its output, or we forcibly close
            # the master
            break

    process.kill()  # Ensure the subprocess is terminated

    # Attempt to extract the runpodctl receive command
    receive_command_match = re.search(r"(runpodctl receive [0-9a-z-]+)", output)
    if receive_command_match:
        return receive_command_match.group(1)
    else:
        return "Could not find the receive command in the output."


# Example usage
your_command = "runpodctl send my-data"
# your_command = "echo Hello, world!"

# This script doesn't work if a zip file already exists locally
receive_command = run_command_and_capture_output(your_command)
print(f"Captured command: {receive_command}")
