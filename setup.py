#!/usr/bin/env python3
import os

from pathlib import Path
from setuptools import setup, find_packages
from setuptools.command.install import install

# Constants have a "_" prefix to reduce the chances to incorrectly import them
# from the code (pauperformance_bot): the IDE will correctly suggest values
# from pauperformance_bot.constant and exclude those defined below.
_HERE = os.path.abspath(os.path.dirname(__file__))
_REQUIREMENTS_DIR = "requirements"
_RESOURCES_DIR = "resources"
_README_FILE = "README.md"
_VERSION_FILE = "VERSION"
_PAUPERFORMANCE_BOT_DIR = Path().joinpath(
    Path.home().as_posix(), ".pauperformance"
).as_posix()
_CACHE_DIR = Path().joinpath(_PAUPERFORMANCE_BOT_DIR, "cache").as_posix()
_STORAGE_DIR = Path().joinpath(_PAUPERFORMANCE_BOT_DIR, "storage").as_posix()
_DECKS_PATH = Path().joinpath(_STORAGE_DIR, "decks").as_posix()
_DECKSTATS_DECKS_PATH = Path().joinpath(_DECKS_PATH, "deckstats").as_posix()
_MTGGOLDFISH_DECKS_PATH = Path().joinpath(_DECKS_PATH, "mtggoldfish").as_posix()


def read_requirements(file_name):
    reqs = []
    with open(os.path.join(_HERE, file_name)) as in_f:
        for line in in_f:
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("    #") \
                    or line.startswith("-r"):
                continue
            reqs.append(line)
    return reqs


with open(os.path.join(_HERE, _README_FILE)) as f:
    readme = f.read()

with open(os.path.join(_HERE, _VERSION_FILE)) as f:
    version = f.read()


def read_resources(resources_dir):
    resources = []
    for root, _, files in os.walk(resources_dir):
        resources.append((f"{root}/", [f"{root}/{file}" for file in files]))
    return resources


class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        os.makedirs(_PAUPERFORMANCE_BOT_DIR, exist_ok=True)
        os.makedirs(_CACHE_DIR, exist_ok=True)
        os.makedirs(_STORAGE_DIR, exist_ok=True)
        os.makedirs(_DECKS_PATH, exist_ok=True)
        os.makedirs(_DECKSTATS_DECKS_PATH, exist_ok=True)
        os.makedirs(_MTGGOLDFISH_DECKS_PATH, exist_ok=True)


setup(
    name="pauperformance-bot",
    version=version,
    url="https://github.com/Pauperformance/pauperformance-bot",
    author="Pauperformance Team",
    author_email=" pauperformance@gmail.com",
    license_files=('LICENSE.txt',),
    description="Myr",
    long_description=readme,
    long_description_content_type="text/markdown",
    python_requires=">=3.7",
    packages=find_packages(exclude=["tests"]),
    install_requires=read_requirements(f"{_REQUIREMENTS_DIR}/requirements.txt"),
    extras_require={
        "test": read_requirements(f"{_REQUIREMENTS_DIR}/requirements-test.txt"),
        "dev": read_requirements(f"{_REQUIREMENTS_DIR}/requirements-dev.txt"),
    },
    data_files=read_resources(_RESOURCES_DIR),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'myr = pauperformance_bot.cli.main:main',
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries",
        # "Typing :: Typed",
    ],
    cmdclass={
        'install': PostInstallCommand,
    },
)
