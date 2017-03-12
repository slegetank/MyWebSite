from flask_sqlalchemy import SQLAlchemy
from .. import db
from flask import url_for

class Blog(db.Model):
    __tablename__ = 'blog'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    type = db.Column(db.String(50))
    writetime = db.Column(db.TIMESTAMP())
    lastupdate = db.Column(db.TIMESTAMP())
    desc = db.Column(db.String(1000))
    image = db.Column(db.String(200))
    filename = db.Column(db.String(100))

    @property
    def format_writetime(self):
        return self.writetime.strftime("%Y-%m-%d %H:%M")

    @property
    def imageArray(self):
        return [url_for('blog.static', filename="MyBlogOrg/static/%s" % image) for image in self.image.split(',')] if len(self.image) != 0 else None

    @property
    def css_type(self):
        if self.type == "Emacs" or self.type == "Book" or self.type == "iOS" or self.type == "Helper":
            return self.type.lower()
        elif self.type == "Software Engineering":
            return "se"
        elif self.type == "History & Politics":
            return "hp"
        else:
            return None

    def __init__(self, id, title, type, writetime, lastupdate, desc, image):
        self.id = id
        self.title = title
        self.type = type
        self.writetime = writetime
        self.lastupdate = lastupdate
        self.desc = desc
        self.image = image

    def __repr__(self):
        return "%s" % self.title
