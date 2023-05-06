import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="stokercloud-client",
    version="0.0.7",
    author="Kristian Øllegaard",
    author_email="kristian@kristian.io",
    description="Python stokercloud client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jacek2511/nbe",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    tests_require=['pytest'],
)
