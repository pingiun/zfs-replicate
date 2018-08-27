# pylint: disable=missing-docstring

from setuptools import setup

setup(
    name="zfs-replicate",
    version="1.0.0",
    description="ZFS Snapshot Replicator",
    url="https://github.com/alunduil/zfs-replicate",

    author="Alex Brandt",
    author_email="alunduil@gmail.com",

    license="BSD-2",

    packages=[
        "zfs.replicate",
        ],

    setup_requires=[
        "pytest-runner",
        ],

    install_requires=[
        "click>=6.7,<6.8",
        "stringcase>=1.2,<1.3",
        ],

    tests_require=[
        "hypothesis",
        "pytest",
        ],

    entry_points = {
        "console_scripts": ["zfs-replicate=zfs.replicate.cli:main",],
        },
    )
