from datetime import datetime
from flask_login import UserMixin, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from . import config


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    header = db.Column(db.String(140))
    title = db.Column(db.String(140))
    title_url = db.Column(db.String(140))
    image_url = db.Column(db.String(140))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    additional_facts = db.relationship('AdditionalFact', backref='author', lazy='dynamic')
    tag_buttons = db.relationship('TagButton', backref='author', lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    shown = db.Column(db.Boolean, default=False)

    def __init__(self, user_id: str, header: str, title: str, title_url: str, image_url: str, body: str):
        self.user_id = user_id
        self.header = header
        self.title = title
        self.title_url = title_url
        self.image_url = image_url
        self.body = body

    def __repr__(self):
        return '<Post {}>'.format(self.title)

    def slack_serialize(self, color, facts, tags):
        return {
            'fallback': self.title,
            'color': color,
            'thumb_url': self.image_url,
            'image_url': self.image_url,
            'pretext': self.header,
            'title': self.title,
            'title_link': self.title_url,
            'text': self.body,
            'fields': [af.slack_serialize() for af in facts],
            'actions': [tb.slack_serialize() for tb in tags],
            'footer': 'aquabot',
            'footer_icon': 'http://s3.amazonaws.com/skyfit-hls/aqua_slack.png'
        }


class AdditionalFact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    text = db.Column(db.String(140))
    is_long = db.Column(db.Boolean)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def __init__(self, post_id: str, title: str, text: str, is_long: bool = True) -> object:
        self.post_id = post_id
        self.title = title
        self.text = text
        self.is_long = is_long

    def serialize(self):
        return {
            'id' : self.id,
            'title' : self.title,
            'text' : self.text,
            'is_long' : self.is_long
        }

    def slack_serialize(self):
        return {
            'title' : self.title,
            'value' : self.text,
            'short' : not self.is_long
        }


class TagButton(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    url = db.Column(db.String(140))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def __init__(self, post_id: str, title: str, url: str):
        self.post_id = post_id
        self.title = title
        self.url = url

    def serialize(self):
        return {
            'id' : self.id,
            'title' : self.title,
            'url' : self.url
        }

    def slack_serialize(self):
        return {
            'type' : 'button',
            'text' : self.title,
            'url' : self.url
        }


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

