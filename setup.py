#!/usr/bin/env python
# coding: UTF-8
# filename: setup.py

"""
setup.py
～～～～～

:author: caorongduan@gmail.com
:copyright: 2017 caorongduan
:license: Apache2, see LICENSE for more details.
"""

from setuptools import setup, find_packages
from showbackup import __version__

with open("README.md", "r") as f:
    long_description = f.read()


def get_requirements():
    with open("requirements.txt") as requirements:
        return (
            [
                line.split("#", 1)[0].strip()
                for line in requirements
                if line and not line.startswith(("#", "--"))
            ],
        )


setup(
    name="showbackup",
    version=__version__,
    author="caorongduan",
    author_email="caorongduan@gmail.com",
    description="A MySQL backup tool, Simple, Fast and Powerful. 一个简单，高效，强大的MySQL备份工具。",
    license="Apache 2.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/caorongduan/showbackup",
    packages=find_packages(),
    include_package_data=True,
    install_requires=get_requirements(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: System :: Archiving :: Backup",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    entry_points="""
        [console_scripts]
        showbackup=showbackup.main:cli
    """,
)
