#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: zhuima
# zhuima @ 2019-01-08 20:01:46
# Function: 

from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect


bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
moment = Moment()


@login_manager.user_loader
def load_user(user_id):
    from fladkipa.models import User
    user = User.query.get(int(user_id))
    return user


login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'warning'
