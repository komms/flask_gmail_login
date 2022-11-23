from flask import Flask, url_for, render_template, redirect, session
from authlib.integrations.flask_client import OAuth

# OAuth 
oauth = OAuth()

oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)
