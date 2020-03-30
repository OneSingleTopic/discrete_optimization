import setuptools

with open("README.adoc", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="my_solvers",
    version="0.1",
    scripts=["my_solvers/solvers.py"],
    author="Max",
    author_email="max",
    description="Solver for Coursera class",
    long_description=long_description,
    long_description_content_type="text/asciidoc",
    url="https://github.com/javatechy/dokr",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["numpy"],
    extras_require={"dev": ["black", "jupyter", "pytest"]},
)
