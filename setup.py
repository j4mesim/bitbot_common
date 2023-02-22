from os.path import join, dirname

from setuptools import setup

__version__ = open(join(dirname(__file__), "common", "__version__")).read().strip()

install_requires = [line.strip() for line in open("requirements.txt", "r").readlines()]

setup(
    name="common",
    version=__version__,
    description="Bitbot Common package utils",
    author="James McDonald",
    author_email="j4mesmcdonald@gmail.com",
    install_requires=install_requires,
    packages="common".split(),
    include_package_data=True,
)
