#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: zhuima
# zhuima @ 2019-01-08 20:00:59
# Function: 


import ldap
import os
from flask import current_app
from flaskipa.extensions import db


def get_ldap_connection():
    #conn = ldap.initialize(os.getenv('LDAP_PROVIDER_URL'))
    conn = ldap.initialize(current_app.config['LDAP_PROVIDER_URL'])
    return conn

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))

    def __init__(self, username, password):
        self.username = username

    @staticmethod
    def try_login(username, password):
        conn = get_ldap_connection()
        conn.simple_bind_s(
            'uid=%s,cn=users,cn=accounts,dc=zy,dc=cn' % username, password
        )

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)
