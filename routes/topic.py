from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from models.board import Board
from models.reply import Reply
from models.user import User
from routes import current_user, csrf_required, new_csrf_token, login_required, topic_owner_required

from models.topic import Topic


main = Blueprint('boyka_topic', __name__)


@main.route("/")
@login_required
def index():
    board_id = int(request.args.get('board_id', -1))
    if board_id == -1:
        ms = Topic.all()
    else:
        ms = Topic.all(board_id=board_id)
    bs = Board.all()
    u = current_user()
    token = new_csrf_token()
    return render_template("topic/index.html", ms=ms, token=token, u=u, bs=bs, bid=board_id)


@main.route('/<int:id>')
def detail(id):
    # http://localhost:3000/topic/1
    m = Topic.get(id)
    u = current_user()
    # 不应该放在路由里面
    # m.views += 1
    # m.save()

    # 传递 topic 的所有 reply 到 页面中
    return render_template("topic/detail.html", topic=m, u=u)


@main.route("/add", methods=["POST"])
@csrf_required
def add():
    form = request.form.to_dict()
    u = current_user()
    print('currentuser', u)
    m = Topic.new(form, user_id=u.id)
    return redirect(url_for('.detail', id=m.id))

@main.route("/delete")
@topic_owner_required
@csrf_required
def delete():
    id = int(request.args.get('id'))
    u = current_user()
    print('删除 topic 用户是', u, id)
    Topic.delete(id)
    return redirect(url_for('.index'))


@main.route("/new")
def new():
    u = current_user()
    board_id = int(request.args.get('board_id'))
    bs = Board.all()
    token = new_csrf_token()
    return render_template("topic/new.html", bs=bs, bid=board_id, token=token, u=u)


@main.route("/profile/<int:id>")
def profile(id):
    u = User.one(id=id)
    topics = Topic.all_desc_order(user_id=id)
    replies = Reply.all_desc_order(user_id=id)
    rtopics = []
    for reply in replies:
        topic = Topic.one(id=reply.topic_id)
        if topic in rtopics:
            continue
        rtopics.append(topic)
    return render_template("topic/profile.html", u=u, topics=topics, rtopics=rtopics)


