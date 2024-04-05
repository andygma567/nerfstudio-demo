"""
This file contains test functions for the example workflow.

To test the task inside of a workflow, you can use the flyte.testing module.
For testing the logic of the workflow, it is a good practice to use mocked tasks
and check that the logic holds.

You may also need to write an end-to-end test later. However, it is unclear how to
end-to-end test the result of runpod.
"""

from workflows.example import preprocess_data, send_data
import os
import glob


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
