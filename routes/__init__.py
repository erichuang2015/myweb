import uuid
from functools import wraps

from flask import (
    request,
    redirect,
    url_for,
    session,
    abort,
    flash,
)

from models.todo import Todo
from models.token import Token
from models.topic import Topic
from models.user import User
from utils import log


def current_user():
    uid = session.get('user_id', '-1')
    if uid == '-1':
        u = User.guest()
    else:
        u = User.one(id=uid)
    return u


def csrf_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args['token']
        u = current_user()
        t = Token.one(csrf_token=token)
        if t.user_id == u.id:
            Token.delete(id=t.id)
            log('删除了token')
            return f(*args, **kwargs)
        else:
            abort(401)

    return wrapper


def new_csrf_token():
    u = current_user()
    Token.pop_exist(user_id=u.id)
    token = str(uuid.uuid4())
    form = dict(
        csrf_token=token, user_id=u.id
    )
    t = Token.new(form)
    return t.csrf_token

def login_required(route_function):
    """
    登录权限验证的装饰器函数
    """

    @wraps(route_function)
    def f():
        log('login_required')
        u = current_user()
        if u.is_guest():
            log('游客用户')
            return redirect(url_for('user.login_view'))
        else:
            log('登录用户', route_function)
            return route_function()

    return f

def same_user_required(route_function):
    """
    用于todo的同用户验证的装饰器函数
    """

    @wraps(route_function)
    def f():
        log('same_user_required')
        u = current_user()
        if 'id' in request.args:
            todo_id = request.args['id']
        else:
            form = request.get_json()
            log('form', form)
            todo_id = int(form['id'])
        t = Todo.one(id=int(todo_id))

        if t.user_id == u.id:
            return route_function()
        else:
            return redirect(url_for('todo_view.index'))

    return f

def topic_owner_required(route_function):
    """
    用于topic的权限验证
    """

    @wraps(route_function)
    def f():
        log('topic_owner_required')
        u = current_user()
        if 'id' in request.args:
            topic_id = request.args['id']
        else:
            topic_id = request.get_json()['id']
        t = Topic.one(id=int(topic_id))

        if t.user_id == u.id:
            return route_function()
        else:
            flash('权限不够，只能帖子作者才能更改')
            return redirect(url_for('boyka_topic.index', id=topic_id))

    return f

