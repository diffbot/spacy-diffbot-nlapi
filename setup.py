# coding: utf-8

from setuptools import setup, find_packages

NAME = "spacy-diffbot-nlapi"
VERSION = "1.0.0"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    "spacy>=3",
    "aiohttp>=3.7",
]

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name=NAME,
    version=VERSION,
    description="spaCy wrapper for Diffbot Natural Language API",
    license='MIT',
    author='Jay Schmidek',
    author_email="jay@diffbot.com",
    url="https://github.com/diffbot/spacy-diffbot-nlapi",
    keywords=["Diffbot", "Natural Language API"],
    install_requires=REQUIRES,
    python_requires='>=3.6',
    packages=find_packages(),
    include_package_data=True,
    long_description=long_description,
    long_description_content_type='text/markdown'
)
