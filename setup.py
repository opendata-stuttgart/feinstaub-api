import setuptools

 with open("README.md", "r") as fh:
    long_description = fh.read()

 with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

 setuptools.setup(
    name="feinstaub",
    version="0.0.1",
    author="Feinstaub",
    description="Api to save data from sensors (especially particulates sensors).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/opendata-stuttgart/feinstaub-api",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=install_requires
)