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


## Preview
![demo](screenshot/demo1.png)

![demo](screenshot/demo2.png)

![demo](screenshot/demo3.png)

![demo](screenshot/demo4.png)

