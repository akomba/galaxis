#!/usr/bin/env python
# -*- coding: utf-8 -*-

# For a fully annotated version of this file and what it does, see
# https://github.com/pypa/sampleproject/blob/master/setup.py

# To upload this file to PyPI you must build it then upload it:
# python setup.py sdist bdist_wheel  # build in 'dist' folder
# python-m twine upload dist/*  # 'twine' must be installed: 'pip install twine'

import ast
import io
import re
import os
from setuptools import find_packages, setup

DEPENDENCIES = ['toml','requests']
EXCLUDE_FROM_PACKAGES = ["contrib", "docs", "tests*"]
CURDIR = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(CURDIR, "README.md"), "r", encoding="utf-8") as f:
    README = f.read()


def get_version():
    main_file = os.path.join(CURDIR, "glx", "glx.py")
    _version_re = re.compile(r"__version__\s+=\s+(?P<version>.*)")
    with open(main_file, "r", encoding="utf8") as f:
        match = _version_re.search(f.read())
        version = match.group("version") if match is not None else '"unknown"'
    return str(ast.literal_eval(version))


setup(
    name="galaxis",
    version=get_version(),
    author="Andras Kristof",
    author_email="akristof@galaxis.xyz",
    description="",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com",
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    include_package_data=True,
    keywords=[],
    scripts=["bash_scripts/glxloop"],
    entry_points={"console_scripts": [
        "glx=glx.glx:main",
        "glxsocket=glx.glxsocket:main",
        "communities=glx.communities_cli:main",
        "attributes=glx.attributes_cli:main",
        "members=glx.members_cli:main",
        "scheduler=glx.scheduler_cli:main",
        "leaker=glx.leaker_cli:main"
        ]},
    data_files=[("share/man/man6", ["man/glx.6"])],
    zip_safe=False,
    install_requires=DEPENDENCIES,
    test_suite="tests.test_project",
    python_requires=">=3.6",
    # license and classifier list:
    # https://pypi.org/pypi?%3Aaction=list_classifiers
    license="License :: OSI Approved :: MIT License",
    classifiers=[
        "Programming Language :: Python",
        # "Programming Language :: Python :: 3",
        # "Operating System :: OS Independent",
        # "Private :: Do Not Upload"
    ],
)
