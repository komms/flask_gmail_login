from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)


def init_db_table(app):
    with app.app_context():
        db.create_all()


def add_user(app, id, username, email):
    with app.app_context():
        new_user = User(id=id, username=username, email=email)
        db.session.add(new_user)
        db.session.commit()


def delete_user_with_username(app, username):
    with app.app_context():
        User.query.filter_by(username=username).delete()
        db.session.commit() 


def query_user_with_username(app, username): 
    with app.app_context():
        queried_user = User.query.filter_by(username=username).first()
    return queried_user


def query_all(app):
    with app.app_context():
        all_users = User.query.all()
    return all_users
