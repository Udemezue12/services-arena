from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional, Regexp
from wtforms import StringField, SubmitField, PasswordField, EmailField, SelectField, IntegerField, BooleanField, DateField, TimeField, TextAreaField, FileField
from flask_wtf.file import FileAllowed
from flask_login import current_user
from book.models import User, Service


class LoginForm(FlaskForm):
    # email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UserDetailsForm(FlaskForm):
    profile_pic = FileField('Profile Pic', validators=[Optional(), FileAllowed(
        ['jpg', 'png', 'jpeg'], 'Images Only')])
    certificates = FileField('Certificates', validators=[
        Optional(),
        FileAllowed(['jpg', 'png', 'jpeg', 'pdf'],
                    'Only images or PDFs allowed!')
    ])
    date_of_birth = DateField('Date of Birth', format='%Y-%m-%d', validators=[
        DataRequired(message='Please provide your date of birth.')
    ])
    bio = StringField('Bio', validators=[
        DataRequired(), Length(min=2, max=320)])
    phone_number = StringField('Phone Number', validators=[
        DataRequired(),
        Length(min=10, max=20),
        Regexp(
            r'^\+?[0-9]*$', message='Phone number must contain only numbers and optionally start with a plus.')
    ])
    submit = SubmitField('Submit')


class ProviderRegsiterForm(FlaskForm):
    role = SelectField(
        'Role', choices=[('provider', 'Provider')], validators=[DataRequired()], default='provider')
    full_name = StringField('First Name', validators=[
        DataRequired(), Length(min=2, max=320)])
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=200)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


class CustomerRegsiterForm(FlaskForm):
    role = SelectField(
        'Role', choices=[('customer', 'Customer')], validators=[DataRequired()], default='customer')
    full_name = StringField('First Name', validators=[
        DataRequired(), Length(min=2, max=320)])

    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=200)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


class AdminRegsiterForm(FlaskForm):
    role = SelectField(
        'Role', choices=[('admin', 'Admin')], validators=[DataRequired()], default='admin')
    full_name = StringField('First Name', validators=[
        DataRequired(), Length(min=2, max=320)])
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=200)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(
                'There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


class ServiceForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    country = SelectField('Country', validators=[DataRequired()], validate_choice=False)
    state = SelectField('State', choices=[], validators=[DataRequired()], validate_choice=False)
    price = StringField('Price', validators=[DataRequired()])
    submit = SubmitField('Create Service')



class BookingForm(FlaskForm):
    date = DateField('Select Date', format='%Y-%m-%d', validators=[DataRequired()])
    start_time = TimeField('Start Time', validators=[DataRequired()])
    end_time = TimeField('End Time', validators=[DataRequired()])
    submit = SubmitField('Submit Booking')

class AvailabilityForm(FlaskForm):
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    start_time = TimeField('Start Time', format='%H:%M',
                           validators=[DataRequired()])
    end_time = TimeField('End Time', format='%H:%M',
                         validators=[DataRequired()])
    country = SelectField('Country', validators=[
                          DataRequired()], validate_choice=False)
    service = SelectField('Service', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Check Services Available')

    def __init__(self, *args, **kwargs):

        super(AvailabilityForm, self).__init__(*args, **kwargs)
        self.service.choices = [(service.id, service.name) for service in Service.query.filter_by(
            provider_id=current_user.id).all()]




class AppointmentForm(FlaskForm):
    user_name = StringField('User Name', validators=[DataRequired()])
    user_id = IntegerField('User ID', validators=[DataRequired()])
    
    service_id = SelectField('Service', choices=[], coerce=int, validators=[DataRequired()])  
    service_name = StringField('Service Name', validators=[DataRequired()])

    date = DateField('Date', validators=[DataRequired()], format='%Y-%m-%d')
    start_time = TimeField('Start Time', validators=[DataRequired()], format='%H:%M:%S')
    end_time = TimeField('End Time', validators=[DataRequired()], format='%H:%M:%S')

    status = SelectField(
        'Status', 
        choices=[
            ('Pending', 'Pending'), 
            ('Confirmed', 'Confirmed'),
            ('Cancelled', 'Cancelled'), 
            ('Completed', 'Completed')
        ], 
        default='Pending'
    )
    
    submit = SubmitField('Book Appointment')

    def validate_end_time(self, end_time):
        if self.start_time.data >= end_time.data:
            raise ValidationError("End time must be after start time.")



class NotificationForm(FlaskForm):
    user_name = StringField('User Name', validators=[DataRequired()])
    user_id = IntegerField('User ID', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    is_read = BooleanField('Read')
    submit = SubmitField('Send Notification')

class ComplaintForm(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired(), Length(max=150)])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send Complaint')
