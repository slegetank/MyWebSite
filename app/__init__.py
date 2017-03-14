from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__, static_folder="static")

    # main
    from main import main

    # blog
    from blog import blog
    if config_name == "debug":
        os.environ['MYWEBSITE_HOST'] = "slegetank.com"
        app.register_blueprint(blog, url_prefix='/blogs')
        app.register_blueprint(main)
    elif config_name == "release":
        app.config['SERVER_NAME'] = 'slegetank.com'
        app.url_map.default_subdomain="www"
        app.config['SESSION_COOKIE_DOMAIN'] = 'slegetank.com'

        app.register_blueprint(blog, subdomain="blog")
        app.register_blueprint(main)

        os.environ['MYWEBSITE_HOST'] = "localhost"

    os.environ['MYWEBSITE_DB_PASS'] = "Wiimu123456"

    # db
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:%s@%s/mywebsite?charset=utf8' % (os.getenv('MYWEBSITE_DB_PASS'), os.getenv('MYWEBSITE_HOST'))
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    return app
