import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="di",
    version="0.0.1",
    author="Dima Kajola",
    author_email="dima.kajola@gmail.com",
    description="A small package that resolves dependency injections via methods' annotations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DimaKajola/di",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
