from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, TimeField, DateField, ValidationError, IntegerField, TextAreaField, BooleanField
from wtforms.validators import DataRequired

from book.models import Service



class ServiceForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    country = SelectField('Country', validators=[DataRequired()], validate_choice=False)
    price = StringField('Price', validators=[DataRequired()])
    submit = SubmitField('Create Service')


class AvailabilityForm(FlaskForm):
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    start_time = TimeField('Start Time', format='%H:%M', validators=[DataRequired()])
    end_time = TimeField('End Time', format='%H:%M', validators=[DataRequired()])
    country = SelectField('Country', validators=[DataRequired()], validate_choice=False)
    service = SelectField('Service', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Check Services Available')

    def __init__(self, *args, **kwargs):
        
        super(AvailabilityForm, self).__init__(*args, **kwargs)
        self.service.choices = [(service.id, service.name) for service in Service.query.filter_by(provider_id=current_user.id).all()]

    
class AppointmentForm(FlaskForm):
    user_name = StringField('User Name', validators=[DataRequired()])
    user_id = IntegerField('User ID', validators=[DataRequired()])
    service_id = SelectField('Service', choices=[], coerce=int, validators=[DataRequired()])  # Changed to SelectField for choices
    service_name = StringField('Service Name', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()], format='%Y-%m-%d')
    start_time = TimeField('Start Time', validators=[DataRequired()], format='%H:%M:%S')
    end_time = TimeField('End Time', validators=[DataRequired()], format='%H:%M:%S')
    status = SelectField('Status', choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), 
                                            ('Cancelled', 'Cancelled'), ('Completed', 'Completed')], default='Pending')
    submit = SubmitField('Book Appointment')

    def validate_end_time(self, end_time):
        if self.start_time.data >= end_time.data:
            raise ValidationError("End time must be after start time.")

class NotificationForm(FlaskForm):
    user_name = StringField('User Name', validators=[DataRequired()])
    user_id = IntegerField('User ID', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    read = BooleanField('Read')  
    submit = SubmitField('Send Notification')