#!/usr/bin/env python

"""The setup script."""

from setuptools import find_packages, setup

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = [
    "Click>=7.0",
]

test_requirements = [
    "pytest>=3",
]

setup(
    author="Chris Winikka",
    author_email="cwinikka@gmail.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description=(
        "This project is designed to assess students' "
        "ability to code clean, semantic front-end technologies "
        "(HTML, CSS, JavaScript) for a "
        "variety of open-ended tasks and projects."
    ),
    entry_points={
        "console_scripts": [
            "webanalyst=webanalyst.cli:main",
        ],
    },
    install_requires=requirements,
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="webanalyst",
    name="webanalyst",
    packages=find_packages(),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/hundredvisionsguy/webanalyst",
    version="0.5.0",
    zip_safe=False,
)
