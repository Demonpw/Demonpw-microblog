from app import db,login  #db是在app/__init__.py生成的关联后的SQLAlchemy实例
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime
from flask_login import UserMixin
import bleach
from markdown import markdown
from sqlalchemy import Boolean
"""Post = db.Table('Post',
    db.Column('id',db.Integer, primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('user_to_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('content',db.String(400)),
    db.Column('timestamp',db.DateTime, index=True,default=datetime.utcnow),
    db.Column('article_id',db.Integer,db.ForeignKey('article.id')),
    db.Column('is_appear',db.Boolean()),
    db.Column('reply_id',db.Integer,index=True)
)"""
class Post(db.Model):#评论，一个用户对应多个评论
    __tablename__='posts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),index=True)#外键
    user_to_id = db.Column(db.Integer,db.ForeignKey('users.id'),index=True)#外键
    content = db.Column(db.String(400))#内容
    timestamp = db.Column(db.DateTime, index=True,default=datetime.utcnow)
    article_id = db.Column(db.Integer,db.ForeignKey('article.id'),index=True)#外键
    is_appear = db.Column(db.Boolean())
    reply_id = db.Column(db.Integer,index=True)
    #reply_to_userid = db.Column(db.Integer,index=True)

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(320), unique=True)
    password_hash = db.Column(db.String(128))
    user_to_id=db.relationship('Post',foreign_keys=[Post.user_to_id],backref=db.backref('user_to', lazy='joined'),lazy='dynamic',cascade='all, delete-orphan')
    posts=db.relationship('Post',foreign_keys=[Post.user_id],backref=db.backref('userid', lazy='joined'),lazy='dynamic',cascade='all, delete-orphan')
    address = db.Column(db.String(80))#网址


    """followed = db.relationship('Follow',foreign_keys=[Follow.follower_id],
                                      backref=db.backref('follower', lazy='joined'),
                                              lazy='dynamic',
                                              cascade='all, delete-orphan')

    followers = db.relationship('Follow',foreign_keys=[Follow.followed_id],
                                       backref=db.backref('followed', lazy='joined'),
                                               lazy='dynamic',
                                               cascade='all, delete-orphan')"""

    #user_to_id = db.relationship('User', secondary=Post,primaryjoin=(Post.c.user_id == id),secondaryjoin=(Post.c.user_to_id == id),backref=db.backref('Post', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<User{}>'.format(self.username)
    def  set_password(self,password):
        self.password_hash=generate_password_hash(password)
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    body=db.Column(db.Text)
    body_html = db.Column(db.Text)
    create_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    seo_link = db.Column(db.String(128))
    pic_path = db.Column(db.String(320))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    posts = db.relationship('Post',backref='article',lazy='dynamic')
    
    #将文本转化为html
    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p', 'img', 'video', 'div', 'iframe', 'p', 'br', 'span', 'hr', 'src', 'class']
        allowed_attrs = {'*': ['class'],
                        'a': ['href', 'rel'],
                        'img': ['src', 'alt']}
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, attributes=allowed_attrs, strip=True))
db.event.listen(Article.body, 'set', Article.on_changed_body)

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(32), unique=True, index=True,
        nullable=False)
    articles = db.relationship('Article', backref='category', lazy='dynamic')
    number = db.Column(db.Integer)
    # 可以添加一个generate_fake函数，用来测试的时候生成假的分类
    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed, randint
        import forgery_py
        seed()
        for i in range(count):
            t = Category(name=forgery_py.lorem_ipsum.word())
            db.session.add(t)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
    def __repr__(self):
        return '<Category %r>' % self.name