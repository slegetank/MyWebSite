#!/usr/bin/python
# -*- coding: utf-8 -*-

from . import main
import os
import sys
from flask import render_template, request, url_for, send_from_directory
from sqlalchemy import desc
import json

reload(sys)
sys.setdefaultencoding('utf-8')

PAGE_COUNT = 5

@main.route('/')
def index():
    return "Building..."
