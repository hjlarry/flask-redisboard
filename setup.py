"""
    Flask-Redisboard
    ~~~~~~~~~~~~~~
    A flask extension to support user view and manage redis with beautiful interface.
    :author: hjlarry<ultrahe@gmail.com>
    :copyright: (c) 2019 by hjlarry.
    :license: MIT, see LICENSE for more details.
"""
from setuptools import setup
import pathlib

current_dir = pathlib.Path(__file__).parent
with open(current_dir / "README.md", encoding="utf-8") as f:
    long_description = f.read()
with open(current_dir / "flask_redisboard" / "VERSION", encoding="utf-8") as f:
    version = f.read().strip()


setup(
    name="Flask-Redisboard",
    version=version,
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
    entry_points={"console_scripts": ["redisboard=flask_redisboard.example:main",]},
    python_requires=">=3.6",
)
