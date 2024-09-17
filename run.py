from flask_migrate import Migrate
from book import create_app, db, socketio
from flask_wtf import CSRFProtect
from book.users.routes import auth, core, booking_system
from book.error_pages.handlers import error_pages
# from book.chat.routes import booking_system

app = create_app()

app.register_blueprint(auth, template_folder='book/templates/', static_folder='book/static/')
app.register_blueprint(core, template_folder='book/templates/', static_folder='book/static/')
app.register_blueprint(booking_system, template_folder='book/templates/', static_folder='book/static/')
app.register_blueprint(error_pages, template_folder='book/templates/', static_folder='book/static/')
# app.register_blueprint(booking_system, template_folder='book/templates/', static_folder='book/static/')
migrate = Migrate(app, db)


if __name__ == '__main__':
    app.run(debug=True, port=3000)
