import setuptools

with open("README", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vamdclib",
    version="0.3",
    author="Christian Endres, Jacob Laas",
    author_email="jclaas@gmail.com",
    description="A pure-python library for the VAMDC.",
    long_description=long_description,
    long_description_content_type="text/plain",
    url="https://github.com/notlaast/vamdclib",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPLv3 License",
        "Operating System :: Linux",
        "Operating System :: Windows",
        "Operating System :: MacOS"
    ],
)