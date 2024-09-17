from flask import Flask
import os
from book.extensions import db, migrate, login_manager, socketio, cors, csrf, mail, bcrypt
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    socketio.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app)

    with app.app_context():
        from book.models import User, Appointment, Service, Notification, Review

   

    

    return app


login_manager.login_view = 'auth.login'
login_manager.refresh_view = 'auth.login'
login_manager.needs_refresh_message = 'You need to Login Again'
