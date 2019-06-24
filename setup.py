"""
    Flask-Redisboard
    ~~~~~~~~~~~~~~
    A flask extension to support user view and manage redis with beautiful interface.
    :author: hjlarry<ultrahe@gmail.com>
    :copyright: (c) 2019 by hjlarry.
    :license: MIT, see LICENSE for more details.
"""
from os import path
from codecs import open
from setuptools import setup

basedir = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(basedir, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="Flask-Redisboard",
    version="0.1.1",
    url="https://github.com/hjlarry/flask-redisboard",
    license="MIT",
    author="hjlarry",
    author_email="ultrahe@gmail.com",
    description="A flask extension to support user view and manage redis with beautiful interface.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    platforms="any",
    packages=["flask_redisboard"],
    zip_safe=False,
    include_package_data=True,
    install_requires=["Flask", "redis"],
    extras_require={"dev": ["black"]},
    keywords="flask extension development redis",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
