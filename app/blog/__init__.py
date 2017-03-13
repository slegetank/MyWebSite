from flask import Blueprint

blog = Blueprint('blog', __name__, template_folder='blog_templates', static_folder='blog_static')

from . import views, errors
