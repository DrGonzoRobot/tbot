from distutils.core import setup
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='tbot',
    version='4.3.3',
    license='MIT',
    long_description=long_description,
    packages=setuptools.find_packages()
)
