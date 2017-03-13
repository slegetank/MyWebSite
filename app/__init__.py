from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__, static_folder=None)

    # main
    from main import main
    app.register_blueprint(main)

    # blog
    from blog import blog
    if config_name == "debug":
        os.environ['MYWEBSITE_HOST'] = "slegetank.com"
        app.register_blueprint(blog, url_prefix='/blogs')
    elif config_name == "release":
        app.config['SERVER_NAME'] = 'slegetank.com'
        app.url_map.default_subdomain="www"
        app.static_url_path = "/static"
        app.static_folder = "static"
        app.add_url_rule(app.static_url_path + '/<path:filename>',
                         endpoint='static',
                         view_func=app.send_static_file,
                         subdomain="static")
        app.register_blueprint(blog, subdomain="blog")

        os.environ['MYWEBSITE_HOST'] = "localhost"

    os.environ['MYWEBSITE_DB_PASS'] = "Wiimu123456"

    # db
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:%s@%s/mywebsite?charset=utf8' % (os.getenv('MYWEBSITE_DB_PASS'), os.getenv('MYWEBSITE_HOST'))
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    return app
