#!/usr/bin/python
# -*- coding: utf-8 -*-

from . import blog
import os
import sys
from flask import render_template, request, url_for, send_from_directory
import modles
from sqlalchemy import desc
import json

reload(sys)
sys.setdefaultencoding('utf-8')

PAGE_COUNT = 5

@blog.route('/')
def index():
    fromIndex = request.args.get("from", 0, type=int)
    count = request.args.get("count", PAGE_COUNT, type=int)
    blogtype = request.args.get("blogtype", "")

    blogs = None
    if not blogtype:
        blogs = modles.Blog.query.order_by(desc(modles.Blog.writetime)).offset(fromIndex).limit(count)
    else:
        blogs = modles.Blog.query.filter_by(type=blogtype).order_by(desc(modles.Blog.writetime)).offset(fromIndex).limit(count)

    if fromIndex == 0:
        return render_template("index.html",
                               PAGE_COUNT=PAGE_COUNT,
                               blogs=blogs,
                               moreurl=url_for("blog.index", _external=True),
                               typeurl=url_for("blog.index", _external=True),
                               count=blogs.count(),
                               blogtype=blogtype)

    return json.dumps({"count": blogs.count(),
                       "data": render_template("index_more.html",
                                               PAGE_COUNT=PAGE_COUNT,
                                               blogs=blogs,
                                               typeurl=url_for("blog.index", _external=True),
                                               count=blogs.count(),
                                               blogtype=blogtype),
                       "blogtype":blogtype})

@blog.route('/article/<orgname>')
def article(orgname):
    orgPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static/MyBlogOrg/blog/%s" % orgname)

    if orgname and os.path.exists(orgPath):
        return render_template("article.html", orgurl=url_for("blog.static", filename="MyBlogOrg/blog/%s" % orgname))

    return "404"
