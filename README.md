# nerfstudio-demo
Code for using nerfstudio and nerf models

### Notes to self
Running `pip install nerfstudio` with the latest version of python (3.12) leads to some kind of problem with the build wheel. 

But running the same command with a python 3.8 command appears to work... I don't know why. However, Flyte also is compatible with python 3.8 so maybe this is okay. 

Processing the record 3d data really is much faster. I didn't benchmark this though... I need to use the folder that contains the depth and rgb subdirectories.

I should try to see if python==3.11.* works for installing the nerfstudio package.  