from sqlalchemy import Column, String

import secret
from models.base_model import SQLMixin, db
from models.user_role import UserRole


class User(SQLMixin, db.Model):
    __tablename__ = 'User'
    """
    User 是一个保存用户数据的 model
    """

    username = Column(String(50), nullable=False)
    password = Column(String(256), nullable=False)
    image = Column(String(100), nullable=False, default='/images/333.jpg')
    signature = Column(String(256), nullable=False, default='"这个家伙懒，什么个性签名都没有。"')
    email = Column(String(50), nullable=False, default=secret.test_mail)
    role = Column(String(10),nullable=False, default=UserRole.normal)

    @staticmethod
    def guest():

        form = dict(
            role=UserRole.guest,
            username='【游客】',
            password='【游客】',
        )
        u = User.new(form)
        return u

    def is_guest(self):
        return self.role == UserRole.guest

    @classmethod
    def salted_password(cls, password, salt='$!@x>K<?>I&D?Wt`'):
        import hashlib
        def sha256(ascii_str):
            return hashlib.sha256(ascii_str.encode('ascii')).hexdigest()
        hash1 = sha256(password)
        hash2 = sha256(hash1 + salt)
        print('sha256', len(hash2))
        return hash2

    def hashed_password(self, pwd):
        import hashlib
        # 用 ascii 编码转换成 bytes 对象
        p = pwd.encode('ascii')
        s = hashlib.sha256(p)
        # 返回摘要字符串
        return s.hexdigest()

    @classmethod
    def register(cls, form):
        name = form.get('username', '')
        safe_form = {}
        print('register', form)
        if len(name) > 2 and User.one(username=name) is None:
            safe_form['username'] = name
            safe_form['password'] = User.salted_password(form['password'])
            u = User.new(safe_form)
            return u
        else:
            return None

    @classmethod
    def validate_login(cls, form):
        query = dict(
            username=form['username'],
            password=User.salted_password(form['password']),
        )
        print('validate_login', form, query)
        return User.one(**query)
