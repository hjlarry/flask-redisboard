"""
    Flask-Redisboard
    ~~~~~~~~~~~~~~
    A flask extension to support user view and manage redis with beautiful interface.
    :author: hjlarry<ultrahe@gmail.com>
    :copyright: (c) 2019 by hjlarry.
    :license: MIT, see LICENSE for more details.
"""
from setuptools import setup


long_description = """
# flask-redisboard

A flask extension to support user view and manage redis with beautiful interface.


## Get Started

Installation is easy:
```
$ pip install flask-redisboard
```

Initialize the extension:
```
from flask_redisboard import RedisBoardExtension
...
board = RedisBoardExtension(app)
```

Also support for factory pattern:
```
from flask_redisboard import RedisBoardExtension
board = RedisBoardExtension()

def create_app():
    app = Flask(__name__)
    ...
    board.init_app(app)
```

Now, you can go to 127.0.0.1:5000/redisboard 
"""


setup(
    name="Flask-Redisboard",
    version="0.1.5",
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
