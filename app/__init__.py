from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:%s@%s/mywebsite?charset=utf8' % (os.getenv('MYWEBSITE_DB_PASS'), os.getenv('MYWEBSITE_HOST'))
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # main
    from main import main
    app.register_blueprint(main)

    # blog
    from blog import blog
    if config_name == "debug":
        app.register_blueprint(blog, url_prefix='/blogs')
    elif config_name == "release":
        app.url_map.default_subdomain="www"
        app.config['SERVER_NAME'] = 'slegetank.com'
        app.register_blueprint(blog, subdomain="blog")

    return app
