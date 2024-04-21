"""
This file contains test functions for the example workflow.

To test the task inside of a workflow, you can use the flyte.testing module.
For testing the logic of the workflow, it is a good practice to use mocked tasks
and check that the logic holds.

You may also need to write an end-to-end test later. However, it is unclear how to
end-to-end test the result of runpod.

These tests could be improved by using fixtures to set up the test data and clean up. 
For example, you could use a fixture to copy the test data to a temporary directory and
then use a teardown feature to clean up the generated zip files.
"""

from flytekit.testing import task_mock
from unittest import mock
from unittest.mock import Mock
from src.workflows.example import preprocess_data, send_data, trigger_runpod, wf
from src.workflows import example
import os
import glob
import pytest


def test_preprocess_data():
    """
    Test the preprocess_data function.

    This test verifies that the returned directory is not empty and contains the
    expected subdirectories and transforms.json file.

    Returns:
        None
    """

    # Arrange
    raw_data_dir = (
        "/Users/andrewma/Desktop/nerfstudio-demo/2024-03-17--18-25-12/EXR_RGBD"
    )
    # Act

    # When executing a flyte workflow locally, such as with a test then the
    # flyte.current_context() will return None use the temporary directory of the local
    # machine. In the Mac OS case this is in the vars/ directory

    preprocessed_data_dir = preprocess_data(raw_data_dir=raw_data_dir)
    path = preprocessed_data_dir.path
    # Assert
    assert os.path.isdir(os.path.join(path, "images"))
    assert os.path.isdir(os.path.join(path, "images_2"))
    assert os.path.isdir(os.path.join(path, "images_4"))
    assert os.path.isdir(os.path.join(path, "images_8"))
    assert os.path.isfile(os.path.join(path, "transforms.json"))


def test_send_data(tmp_path):
    """
    Test the send_data function.

    Parameters
    ----------
    tmp_path : str
        The temporary directory path that will be sent.

    Returns
    -------
    None

    Raises
    ------
    AssertionError
        If the output does not contain the expected string.

    Notes
    -----
    This test function verifies the behavior of the send_data function. It sends a
    temporary directory to runpod using and checks if the output contains the expected
    string "runpodctl receive". It also performs cleanup by removing any generated zip
    files.

    In the future, it is recommended to use a fixture to copy the test set data to the
    temporary directory and utilize the teardown feature of fixtures to clean up the
    generated zip files.

    Flyte automatically converts directories to FlyteDirectory objects. For more
    information, refer to the documentation:
    https://docs.flyte.org/en/latest/user_guide/data_types_and_io/index.html
    """
    # Arrange
    # Act
    output = send_data(preprocessed_data=tmp_path)
    # Assert
    assert "runpodctl receive" in output

    # Teardown
    for file in glob.glob("*.zip"):
        os.remove(file)


@pytest.mark.skip(reason="This test requires runpod api to be installed.")
def test_trigger_runpod(monkeypatch):
    # Mock the create_pod method
    mock_create_pod = Mock()
    # Set the return value of the mock_create_pod method
    mock_create_pod.return_value = "a_test_return_value"
    monkeypatch.setattr(example.runpod, "create_pod", mock_create_pod)

    # Call the function
    pod_str = trigger_runpod(api_key="test_api_key", receive_command="test_command")

    # Check that create_pod was called with the correct image_name
    mock_create_pod.assert_called_once_with(
        name="test-pod",
        image_name=mock.ANY,
        gpu_type_id="NVIDIA GeForce RTX 3070",
        env={
            "RECEIVE_COMMAND": "test_command",
            "USERNAME": mock.ANY,
            "PASSWORD": mock.ANY,
            "FLYTE_EXECUTION_ID": mock.ANY,  # We don't know the exact value of this
        },
    )

    # Check that the returned string is not empty
    assert pod_str != ""


def test_wf():
    """
    Test the wf workflow.

    This test is designed to test a flyte workflow named `wf`. The workflow takes an
    input that's a FlyteDirectory of preprocessed data and then outputs a string that
    describes all of the run pod pods that are running.

    Parameters
    ----------
    tmp_path : pathlib.Path
        The temporary directory path for the test.

    Raises
    ------
    AssertionError
        If any of the assertions fail.

    Returns
    -------
    None

    """
    # Arrange
    raw_data_dir = (
        "/Users/andrewma/Desktop/nerfstudio-demo/2024-03-17--18-25-12/EXR_RGBD"
    )

    # Act
    # Call the wf workflow with the input directory The wf should output the string
    # representation of the pods running on runpod
    # We mock the trigger_runpod task to avoid actually triggering a runpod
    with task_mock(trigger_runpod) as mock:
        mock.return_value = "mocked_output"
        wf_output = wf(dir=raw_data_dir)
    print("wf_output: ", wf_output)
    
    # Assert
    assert wf_output != ""

    # Teardown
    for file in glob.glob("*.zip"):
        os.remove(file)