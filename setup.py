import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='restpicamera',  
     version='0.1',
     author="Benedict Diederich",
     author_email="bene.d@gmx.de",
     description="Use your raspberry pi camera over the air",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/openUC2/UC2-RESTPiCam",
     #packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: GPL v3",
         "Operating System :: OS Independent",
     ],
    install_requires=['numpy>=1.16', 'requests', 'pyjson'],  # scikit-tensor-py3 for sktensor
    include_package_data=True,
    #package_dir = {'':'NanoImagingPack'},
    package_data={'restpicamera':['server/*', 'client/*']},
 )