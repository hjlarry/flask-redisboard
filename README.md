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

<table align="center">
    <tr>
        <td align="center">
            <a href="https://raw.githubusercontent.com/hjlarry/flask-redisboard/master/screenshot/demo1.png">
                <img src="screenshot/demo1.png" alt="Screenshot Dashboard" width="480px" />
            </a>
        </td>
        <td align="center">
            <a href="https://raw.githubusercontent.com/hjlarry/flask-redisboard/master/screenshot/demo2.png">
                <img src="screenshot/demo2.png" alt="Screenshot Database" width="480px" />
            </a>
        </td>
    </tr>
    <tr>
        <td align="center">
            <a href="https://raw.githubusercontent.com/hjlarry/flask-redisboard/master/screenshot/demo3.png">
                <img src="screenshot/demo3.png" alt="Screenshot Command" width="480px" />
            </a>
        </td>
        <td align="center">
            <a href="https://raw.githubusercontent.com/hjlarry/flask-redisboard/master/screenshot/demo4.png">
                <img src="screenshot/demo4.png" alt="Screenshot ServerInfo" width="480px" />
            </a>
        </td>
    </tr>
</table>

