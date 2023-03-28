import os

from flask import Flask, url_for, render_template, redirect, session
from authlib.integrations.flask_client import OAuth


import sys
sys.path.append(f"{os.getcwd()}/user_login")  # should be appended

from user_db import db, User, init_db_table, add_user, query_user_with_username, delete_user_with_username, query_all
from user_profile import oauth

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object("config.DevelopmentConfig") # change it to production config when deployed
    
    # db
    db.init_app(app)
    init_db_table(app)

    # oauth
    oauth.init_app(app)


    @app.route('/')
    def homepage():
        if session.get('user'):
            email = session.get('user')['email']
            name = session.get('user')['name']
            # adding a dummy user for testing
            add_user(app, "12345", name, email)
            return f'Hello, you are logged in as {email}'
        else:
            return 'No one is logged in'

    @app.route('/login')
    def login():
        google = oauth.create_client('google')  # create the google oauth client
        redirect_uri = url_for('authorize', _external=True)
        return google.authorize_redirect(redirect_uri)

    @app.route('/logout')
    def logout():
        session.pop('user', None)
        return redirect('/')

    @app.route('/authorize')
    def authorize():
        google = oauth.create_client('google')  # create the google oauth client
        token = google.authorize_access_token()  # Access token from google (needed to get user info)
        session['user'] = token['userinfo']
        return redirect('/')

    return app