import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Plugin Manager",
    version="2.0.0",
    author="Steven Nix",
    author_email="stevencnix@gmail.com",
    description="Simple Plugin Manager Based off of Yapsy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="To be added",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
)