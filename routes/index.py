import os
import uuid

from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    abort,
    send_from_directory,
    flash,
)

from models.user import User

from utils import log

main = Blueprint('index', __name__)


def current_user():
    # 从 session 中找到 user_id 字段, 找不到就 -1
    # 然后用 id 找用户
    # 找不到就返回 None
    uid = session.get('user_id', -1)
    u = User.one(id=uid)
    return u


"""
用户在这里可以
    访问首页
    注册
    登录

"""


@main.route("/")
def index():
    u = current_user()
    return render_template("index.html", user=u)


@main.route("/register", methods=['POST'])
def register():
    form = request.form
    # 用类函数来判断
    u = User.register(form)
    return redirect(url_for('.index'))


@main.route("/login", methods=['POST'])
def login():
    form = request.form
    u = User.validate_login(form)
    if u is None:
        # 转到 topic.index 页面
        return redirect(url_for('boyka_topic.index'))
    else:
        # session 中写入 user_id
        session['user_id'] = u.id
        # 设置 cookie 有效期为 永久
        session.permanent = True
        return redirect(url_for('boyka_topic.index'))


@main.route('/profile')
def profile():
    u = current_user()
    if u is None:
        return redirect(url_for('.index'))
    else:
        return render_template('profile.html', user=u)


@main.route('/user/<int:id>')
def user_detail(id):
    u = User.find(id)
    if u is None:
        abort(404)
    else:
        return render_template('profile.html', user=u)

@main.route('/image/add', methods=['POST'])
def image_add():
    file = request.files['avatar']

    suffix = file.filename.split('.')[-1]
    filename = '{}.{}'.format(str(uuid.uuid4()), suffix)
    path = os.path.join('images', filename)
    file.save(path)

    u = current_user()
    User.update(u.id, image='/images/{}'.format(filename))

    return redirect(url_for('.setting', id=u.id))


@main.route('/images/<filename>')
def image(filename):
    return send_from_directory('images', filename)

@main.route("/setting")
def setting():
    user = current_user()
    u = User.one(id=user.id)
    return render_template('setting.html', u=u)

@main.route("/newusername", methods=["POST"])
def new_username():
    form = request.form.to_dict()
    log('username获取的表格form', form)
    u = current_user()
    User.update(id=u.id, username=form['username'], signature=form['signature'])
    return redirect(url_for('.setting', id=u.id))

@main.route("/newpassword", methods=["POST"])
def new_password():
    form = request.form.to_dict()
    log('password获取的表格form', form)
    u = current_user()
    form['username'] = u.username
    form['password'] = form['old_password']
    user = User.validate_login(form)
    if user is not None:
        User.update(id=u.id, password=User.salted_password(form['new_password']))
        flash('成功更改密码！')
    else:
        flash('当前密码输入错误！')
    return redirect(url_for('.setting', id=u.id))

@main.route("/about")
def about():
    # 添加about页面
    return render_template('about.html')




# def blueprint():
#     main = Blueprint('index', __name__)
#     main.route("/")(index)
#     main.route("/register", methods=['POST'])(register)
#     main.route("/login", methods=['POST'])(login)
#     main.route('/profile')(profile)
#     main.route('/user/<int:id>')(user_detail)
#
#     return main
