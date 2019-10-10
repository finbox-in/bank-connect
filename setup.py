import setuptools

long_description = ""

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="finbox_bankconnect",
    version="0.1.0",
    author="FinBox",
    author_email="tech@finbox.in",
    description="Python library to use Finbox Bank Connect",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/finbox-in/bank-connect-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['requests'],
    python_requires='>=3.4',
)
