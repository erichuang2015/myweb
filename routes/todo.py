from flask import (
    render_template,
    Blueprint,
)
from routes import (
    current_user,
    login_required,
)
from utils import log

main = Blueprint('todo_view', __name__)


@main.route('/')
@login_required
def index():
    """
    todo 首页的路由函数
    """
    return render_template('todo_index.html')