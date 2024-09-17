from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from book.extensions import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))







class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(300), nullable=False, unique=True)
    role = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    password_hash = db.Column(db.String(200), nullable=False)

    last_login = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    def __init__(self, full_name, role, email, username, password):
        self.full_name = full_name
        self.email = email
        self.role = role
        self.username = username
        self.set_password(password) 
        self.role = role
        self.is_active = True 

    def set_password(self, password):
        
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

         

   

    def __repr__(self):
        return f"User({self.username}, {self.role})"


class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True)  
    country = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(150), nullable=False)
    
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    state = db.Column(db.String(100), nullable=True)
    provider_name = db.Column(db.String(300), db.ForeignKey('user.full_name'), nullable=False)  
    provider = db.relationship('User', backref='services', foreign_keys=[provider_name]) 
    price = db.Column(db.Float, nullable=False)
    # is_available = db.Column(db.Boolean, nullable=False, default=True) 
    def __repr__(self):
        return f"Service({self.name})"




class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(300), db.ForeignKey('user.full_name'), nullable=False) 
    service_name = db.Column(db.String(150), db.ForeignKey('service.name'), nullable=False) 
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), default='Pending')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    country = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(100), nullable=True)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Appointment {self.user_name} {self.date} {self.status}>'


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(300), db.ForeignKey('user.full_name'), nullable=False) 
    message = db.Column(db.String(250), nullable=False)
    read = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Notification {self.user_name} {self.read}>'

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(150), db.ForeignKey('service.name'), nullable=False)
    reviewer_name = db.Column(db.String(300), db.ForeignKey('user.full_name'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Review {self.service_name} {self.reviewer_name} {self.rating}'

class User_Details(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.Integer, db.ForeignKey(
        'user.full_name'), unique=True, nullable=False)
    profile_pic = db.Column(db.String(200), nullable=True)
    bio = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    certificates = db.Column(db.String(200), nullable=True)

    date_of_birth = db.Column(db.Date(), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    user = db.relationship(
        'User', backref=db.backref('passenger', uselist=False))



class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    provider_name = db.Column(db.String(100), nullable=True)
    customer_name = db.Column(db.String(100), nullable=True)
    provider_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    admin_name = db.Column(db.String(100), nullable=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    subject = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), default="Pending")
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Complaint {self.provider_name} - {self.subject}>'
