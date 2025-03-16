from setuptools import setup, find_packages

setup(
    name="r1_experimentation",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "litellm>=1.0.0",
    ],
)
