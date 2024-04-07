# nerfstudio-demo
Code for using nerfstudio and nerf models

### Notes to self
Running `pip install nerfstudio` with the latest version of python (3.12) leads to some kind of problem with the build wheel. 

But running the same command with a python 3.8 command appears to work... I don't know why. However, Flyte also is compatible with python 3.8 so maybe this is okay. 

Processing the record 3d data really is much faster. I didn't benchmark this though... I need to use the folder that contains the depth and rgb subdirectories.

I should try to see if python==3.11.* works for installing the nerfstudio package.  

- I think that I have 4th party dependencies and I might need to use pip-tools, or I should use conda installs or poetry. 
    - I'm hoping that because I'm containerizing stuff like micro services then maybe I won't have to deal with dependency management for "large" python projects

After consideration, I think I prefer to use uv (i.e. pip-tools) for it's speed and it's simplicity. 

I also really liked pdm but I don't know enough about python app development at this time to know if I would actually use the important features of pdm. 

I didn't like using poetry. 

I do think I need a python dependency manager because I can't seem to get the latests packages that I want to use in conda.

I want to continue using conda because I can maybe later track CUDA installations too but I'm not strongly opposed to switching to something like pdm later. 

https://lincolnloop.github.io/python-package-manager-shootout/

## Packages to be installed
```python
python=3.11
nerfstudio # compatible with 3.11
# compatible with 3.11, I think it's important to not use pip install -U with this package install 
flytekit 
runpod

# There is some kind of 'transient' dependency issue with nerfstudio and the other
# packages such as runpod or flytekit and botocore Also conda doesn't seem to have these
# packages so I don't know what to do
```

## Testing structure

I'm trying out using a conftest.py file. I think it allows me to run tests from directories other than where the unit test is located becasue pytest will adjust a PATH on the fly? I might need to change this later. I don't know

- https://docs.pytest.org/en/8.0.x/explanation/pythonpath.html
- https://stackoverflow.com/questions/34466027/what-is-conftest-py-for-in-pytest

