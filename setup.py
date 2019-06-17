import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='DataChunks',  
     version='0.1',
     scripts=[] ,
     author="Lucio Anderlini",
     author_email="l.anderlini@gmail.com",
     description="A simple extension to `root_pandas` for stratified sampling.",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/javatechy/dokr",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )

