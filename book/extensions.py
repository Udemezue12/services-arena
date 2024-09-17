from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO



db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
socketio = SocketIO()
mail = Mail()
bcrypt = Bcrypt()
cors = CORS()
csrf = CSRFProtect()
