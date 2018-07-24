from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

import config
import secret

# web framework
# web application
# __main__
from models.base_model import db
from models.reply import Reply
from models.topic import Topic
from models.user import User
from models.todo import Todo
from models.token import Token
from models.message import Messages
from models.board import Board
from routes import index
from utils import log

# 注册蓝图
# 有一个 url_prefix 可以用来给蓝图中的每个路由加一个前缀
# import routes.index as index_view
from routes.index import main as index_routes
from routes.topic import main as topic_routes
from routes.reply import main as reply_routes
from routes.todo import main as todo_routes
from routes.api_todo import main as todo_api
from routes.message import main as mail_routes, mail
from routes.board import main as board_routes

def count(input):
    log('count using jinja filter')
    return len(input)


def configured_app():
    app = Flask(__name__)
    # 设置 secret_key 来使用 flask 自带的 session
    # 这个字符串是啥都行
    app.secret_key = config.secret_key

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:{}@localhost/myweb?charset=utf8mb4'.format(
        secret.database_password
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    mail.init_app(app)

    app.register_blueprint(index_routes)
    app.register_blueprint(topic_routes, url_prefix='/topic')
    app.register_blueprint(reply_routes, url_prefix='/reply')
    app.register_blueprint(todo_routes, url_prefix='/todo')
    app.register_blueprint(board_routes, url_prefix='/board')
    app.register_blueprint(todo_api)
    app.register_blueprint(mail_routes, url_prefix='/mail')

    app.template_filter()(count)

    admin = Admin(app, name='myweb', template_mode='bootstrap3')
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Topic, db.session))
    admin.add_view(ModelView(Reply, db.session))
    admin.add_view(ModelView(Todo, db.session))
    admin.add_view(ModelView(Token, db.session))
    admin.add_view(ModelView(Messages, db.session))
    admin.add_view(ModelView(Board, db.session))
    # Add administrative views here

    return app


# 运行代码
if __name__ == '__main__':
    # app.add_template_filter(count)
    # debug 模式可以自动加载对代码的变动, 所以不用重启程序
    # 自动 reload jinja
    app = configured_app()
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.jinja_env.auto_reload = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    config = dict(
        debug=True,
        host='localhost',
        port=2000,
        threaded=True,
    )
    app.run(**config)