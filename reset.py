from sqlalchemy import create_engine

from app import configured_app
from models.base_model import db
from models.reply import Reply
from models.topic import Topic
from models.user import User
from models.board import Board

import secret


def reset_database():
    url = 'mysql+pymysql://root:{}@localhost/?charset=utf8mb4'.format(secret.mysql_password)
    e = create_engine(url, echo=True)

    with e.connect() as c:
        c.execute('DROP DATABASE IF EXISTS myweb')
        c.execute('CREATE DATABASE myweb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
        c.execute('USE myweb')

    db.metadata.create_all(bind=e)


def generate_fake_date():

    form = dict(
        username='boyka',
        password='123'
    )
    form['password'] = User.salted_password(form['password'])
    u = User.new(form)

    guest_form = dict(
        username='guest',
        password='guest'
    )
    guest_form['password'] = User.salted_password(guest_form['password'])
    guest = User.new(guest_form)

    board_form = dict(
        title='all'
    )
    b = Board.new(board_form)

    with open('markdown_demo.md', encoding='utf8') as f:
        content = f.read()
    topic_form = dict(
        title='markdown demo',
        board_id=b.id,
        content=content
    )

    for i in range(15):
        print('begin topic <{}>'.format(i))
        t = Topic.new(topic_form, u.id)

        reply_form = dict(
            content='reply test',
            topic_id=t.id,
        )
        for j in range(10):
            Reply.new(reply_form, u.id)


if __name__ == '__main__':
    app = configured_app()
    with app.app_context():
        reset_database()
        generate_fake_date()
