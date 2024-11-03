import os
import logging
from datetime import datetime
from dotenv import load_dotenv

from werkzeug.utils import secure_filename
from flask import redirect, render_template, Blueprint, flash, url_for, request, jsonify
from sqlalchemy.exc import IntegrityError
from flask_login import current_user, login_user, logout_user, login_required
from book.extensions import db, csrf
# from book.email_utils import send_mail
from book.models import User, Service, Notification, Appointment, Review, User_Details, Complaint
from book.fetch import states, countries
from .forms import CustomerRegsiterForm, ProviderRegsiterForm, AdminRegsiterForm, LoginForm, ServiceForm, AppointmentForm, NotificationForm, AvailabilityForm, UserDetailsForm, BookingForm, ComplaintForm


# ///////////////////////
# ////////////////////////
logging.basicConfig(level=logging.DEBUG)
load_dotenv()

# //////////////////
# //////////////////


def validate_password(password):
    if not password:
        raise ValueError('Password cannot be empty or None.')
    if len(password) < 8:
        raise ValueError('Password must be at least 8 characters long.')


# ////////////////////////
# ////////////////
core = Blueprint('core', __name__)


@core.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.role == 'customer':
            return redirect(url_for('booking_system.list_services'))
        elif current_user.role == 'provider':
            return redirect(url_for("booking_system.view_provider_services"))
        else:
            return redirect(url_for('core.index'))
        return render_template('index.html')


# ///////////
# //////////
auth = Blueprint('auth', __name__)


@auth.route('/customer/register', methods=['GET', 'POST'])
def customer_register():
    if current_user.is_authenticated:
        return redirect(url_for('core.index'))
    form = CustomerRegsiterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        existing_user = User.query.filter_by(username=username).first()
        existing_user_email = User.query.filter_by(email=email).first()
        if existing_user or existing_user_email:
            flash('Username or Email already exists.', 'danger')
            return redirect(url_for('auth.customer_register'))
        else:
            try:
                salt = os.getenv('SALT')
                if not salt:
                    flash('Server error: salt is not set.', 'danger')
                    return render_template('login.html', title='Login', form=form)
                password = form.password.data + salt
                validate_password(password)

                user = User(
                    full_name=form.full_name.data,
                    role=form.role.data,
                    email=form.email.data,
                    username=form.username.data,
                    password=password
                )

                db.session.add(user)
                db.session.commit()

                if user.is_authenticated:
                    logout_user()

                    return redirect(url_for('auth.user_details', user_name=user.full_name))

                flash('Thanks for registering!', 'success')
                return redirect(url_for('auth.login'))
            except ValueError as e:
                flash(str(e), 'danger')
            except IntegrityError as e:
                db.session.rollback()
                logging.error("IntegrityError occurred: %s", e)
                flash(
                    "An error occurred during registration. Please try again.", 'danger')

    return render_template('customer_register.html', form=form)


@auth.route('/admin/register', methods=['GET', 'POST'])
def admin_register():
    if current_user.is_authenticated:
        return redirect(url_for('core.index'))
    form = AdminRegsiterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        existing_user = User.query.filter_by(username=username).first()
        existing_user_email = User.query.filter_by(email=email).first()
        if existing_user or existing_user_email:
            flash('Username or Email already exists.', 'danger')
            return redirect(url_for('auth.customer_register'))
        else:
            try:
                salt = os.getenv('SALT')
                if not salt:
                    raise ValueError("Server error: salt is not set.")

                password = form.password.data + salt
                validate_password(password)

                user = User(
                    full_name=form.full_name.data,
                    role=form.role.data,
                    email=form.email.data,
                    username=form.username.data,
                    password=password
                )

                db.session.add(user)
                db.session.commit()

                if user.is_authenticated:
                    logout_user()

                    return redirect(url_for('auth.user_details', user_name=user.full_name))

                flash('Thanks for registering!', 'success')
                return redirect(url_for('auth.login'))
            except ValueError as e:
                flash(str(e), 'danger')
            except IntegrityError as e:
                db.session.rollback()
                flash(
                    "An error occurred during registration. Please try again.", 'danger')

    return render_template('admin_register.html', form=form)


@auth.route('/service/provider/register', methods=['GET', 'POST'])
def provider_register():
    if current_user.is_authenticated:
        return redirect(url_for('core.index'))
    form = ProviderRegsiterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        existing_user = User.query.filter_by(username=username).first()
        existing_user_email = User.query.filter_by(email=email).first()
        if existing_user or existing_user_email:
            flash('Username or Email already exists.', 'danger')
            return redirect(url_for('auth.customer_register'))
        else:
            try:
                salt = os.getenv('SALT')
                if not salt:
                    raise ValueError("Server error: salt is not set.")

                password = form.password.data + salt
                validate_password(password)

                user = User(
                    full_name=form.full_name.data,
                    role=form.role.data,
                    email=form.email.data,
                    username=form.username.data,
                    password=password
                )

                db.session.add(user)
                db.session.commit()

                if user.is_authenticated:
                    logout_user()

                flash('Thanks for registering!', 'success')
                return redirect(url_for('auth.login'))
            except ValueError as e:
                flash(str(e), 'danger')
            except IntegrityError as e:
                db.session.rollback()
                flash(
                    "An error occurred during registration. Please try again.", 'danger')

    return render_template('provider_register.html', form=form)






@auth.route('/user/form/<string:user_name>', methods=['GET', 'POST'])
@login_required
def user_details(user_name):
    if not current_user.is_authenticated:
        flash("Please log in to access this page.", "warning")
        return redirect(url_for('auth.login'))

    form = UserDetailsForm()
    if request.method == 'POST' and form.validate_on_submit():
        phone_number = form.phone_number.data
        existing_user_phone = User_Details.query.filter_by(phone_number=phone_number).first()

        if existing_user_phone:
            flash('This phone number has already been used.', 'danger')
            return redirect(url_for('auth.user_details', user_name=user_name))  # Fixed

        try:
            profile_pic_dir = 'book/static/profile_pics'
            certificates_dir = 'book/static/certificates'

            if not os.path.exists(profile_pic_dir):
                os.makedirs(profile_pic_dir)

            if not os.path.exists(certificates_dir):
                os.makedirs(certificates_dir)

            if form.profile_pic.data:
                profile_pic_file = form.profile_pic.data
                profile_pic_filename = secure_filename(profile_pic_file.filename)
                profile_pic_path = os.path.join(profile_pic_dir, profile_pic_filename)
                profile_pic_file.save(profile_pic_path)
            else:
                profile_pic_filename = None

            certificate_filenames = []
            for certificate_file in form.certificates.data:
                if len(certificate_filenames) < 5:
                    certificate_filename = secure_filename(certificate_file.filename)
                    certificate_path = os.path.join(certificates_dir, certificate_filename)
                    certificate_file.save(certificate_path)
                    certificate_filenames.append(certificate_filename)

            user_details = User_Details.query.filter_by(user_name=current_user.full_name).first()
            if not user_details:
                user_details = User_Details(user_name=current_user.full_name)
                user_details.profile_pic = profile_pic_filename
                user_details.certificates = ",".join(certificate_filenames) 
                user_details.date_of_birth = form.date_of_birth.data
                user_details.phone_number = phone_number
                user_details.bio = form.bio.data

                db.session.add(user_details)
                db.session.commit()

                flash('User details submitted successfully!', 'success')
                return redirect(url_for('core.index'))

        except ValueError as e:
            flash(str(e), 'danger')
        except IntegrityError as e:
            db.session.rollback()
            flash('An integrity error occurred. Please ensure your data is correct.', 'danger')

    return render_template('user_details.html', form=form)




@auth.route('/user/details/<string:user_name>', methods=['GET', 'POST'])
@login_required
def user_details_form(user_name):
    if not current_user.is_authenticated:
        flash("Please log in to access this page.", "warning")
        return redirect(url_for('auth.login'))

    user_details = User_Details.query.filter_by(user_name=user_name).first()

    if not user_details:
        flash("No user details found. Please fill out your profile information.", "warning")
        return redirect(url_for('auth.user_details', user_name=user_name))

    return render_template('user_details_form.html', user_details=user_details)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('core.index'))

    form = LoginForm()

    if form.validate_on_submit():
        salt = os.getenv('SALT')
        if not salt:
            flash('Server error: salt is not set.', 'danger')
            return render_template('login.html', title='Login', form=form)

        user = User.query.filter_by(username=form.username.data).first()

        if user:
            entered_password = form.password.data + salt

            if user.check_password(entered_password):
                login_user(user, remember=form.remember.data)

                if user.role == 'customer':
                    return redirect(url_for('booking_system.list_services'))
                elif user.role == 'provider':
                    return redirect(url_for('booking_system.create_service'))
                elif user.role == 'admin':
                    return redirect(url_for('core.index'))
                else:
                    return redirect(url_for('core.index'))
            else:
                flash(
                    'Invalid credentials. Please check your username and password.', 'danger')
                return redirect(url_for('auth.login'))
        else:
            flash('Login Unsuccessful. Please check username and password.', 'danger')
            return redirect(url_for('auth.login'))

    return render_template('login.html', title='Login', form=form)


@auth.route('/user/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')


@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))


# @auth.route('/dashboard', methods=['GET', 'POST'])
# @login_required
# def dashboard():
#     if current_user.role == 'admin':
#         return redirect(url_for('booking_system.admin_dashboard'))
#     elif current_user.role == 'provider':
#         return redirect(url_for('booking_system.provider_dashboard'))
#     elif current_user.role == 'customer':
#         return redirect(url_for('booking_system.provider_dashboad'))
#     else:
#         return redirect(url_for('core.index'))


# ///////////////////////////////
# ////////////////////
# //////////////////////
booking_system = Blueprint('booking_system', __name__)


@booking_system.route('/customer/dashboard')
@login_required
def customer_dashboard():
    return render_template('customer_dashboard.html')


@booking_system.route('/admin/dashboard')
@login_required
def admin_dashboard():
    return render_template('admin_dashboard.html')


@booking_system.route('/provider/dashboard', methods=['GET'])
@login_required
def provider_dashboard():
    notifications = Notification.query.filter_by(
        user_name=current_user.full_name
    ).order_by(Notification.timestamp.desc()).all()

    appointments = Appointment.query.filter_by(
        user_name=current_user.full_name
    ).order_by(Appointment.date.desc()).all()

    services = Service.query.filter_by(
        provider_name=current_user.full_name
    ).all()

    return render_template(
        'provider_dashboard.html',
        notifications=notifications,
        appointments=appointments,
        services=services
    )


@booking_system.route('/services')
def list_services():
    services = Service.query.all()
    return render_template('services.html', services=services)


@booking_system.route('/create/service', methods=['GET', 'POST'])
@login_required
def create_service():
    form = ServiceForm()
    if current_user.role != 'provider':
        flash('Only providers can create services.')
        return redirect(url_for('core.index'))

    if request.method == 'POST':
        selected_country = request.form.get('country')

        form.state.choices = [(state, state)
                              for state in states.get(selected_country, [])]
        form.country.choices = countries

        if form.validate_on_submit():
            service = Service(
                name=form.name.data,
                description=form.description.data,
                country=form.country.data,
                state=form.state.data,
                price=float(form.price.data),
                provider_name=current_user.full_name,
            )
            db.session.add(service)
            db.session.commit()
            flash('Service created successfully', 'success')
            return redirect(url_for('core.index'))

    return render_template('create_service.html', form=form)


@booking_system.route('/edit/service/<service_name>', methods=['GET', 'POST'])
@login_required
@csrf.exempt
def edit_service(service_name):
    if current_user.role != 'provider':
        flash('Only providers can edit services.')
        return redirect(url_for('core.index'))

    service = Service.query.filter_by(name=service_name).first_or_404()

    if service.provider_name != current_user.full_name:
        flash('You do not have permission to edit this service.', 'danger')
        return redirect(url_for('booking_system.view_provider_services'))

    form = ServiceForm()

    if request.method == 'POST':

        selected_country = request.form.get('country')
        form.state.choices = [(state, state)
                              for state in states.get(selected_country, [])]
        form.country.choices = [(country, country) for country in countries]

    if form.validate_on_submit():
        service.name = form.name.data
        service.description = form.description.data
        service.country = form.country.data
        service.state = form.state.data
        service.price = float(form.price.data)

        db.session.commit()
        flash('Service updated successfully', 'success')
        return redirect(url_for('booking_system.view_provider_services'))
    elif request.method == 'GET':
        form.name.data = service.name
        form.description.data = service.description
        form.country.data = service.country
        form.state.data = service.state
        form.price.data = service.price

    return render_template('edit_service.html', form=form, service=service)


@booking_system.route('/book/service/<string:service_name>', methods=['GET', 'POST'])
@login_required
def book_service(service_name):
    if current_user.role != 'customer':
        flash('Only customers can book.')
        return redirect(url_for('core.index'))
    service = Service.query.filter_by(name=service_name).first()
    if service is None:
        flash('No Services were found.', "danger")
        return redirect(url_for('core.index'))

    provider = User.query.filter_by(full_name=service.provider_name).first()

    if provider is None:
        flash('No service provider was found.', "danger")
        return redirect(url_for('core.index'))

    provider_details = User_Details.query.filter_by(
        user_name=provider.full_name).first()

    existing_appointment = Appointment.query.filter_by(
        user_name=current_user.full_name, service_name=service_name).first()

    if existing_appointment:
        flash('You have already booked this service.', "warning")
        return redirect(url_for('core.index'))

    form = BookingForm()

    if form.validate_on_submit():
        try:
            appointment = Appointment(
                user_name=current_user.full_name,
                service_name=service.name,
                date=form.date.data,
                start_time=form.start_time.data,
                end_time=form.end_time.data,
                status='Pending',
                country=service.country,
                state=service.state
            )

            db.session.add(appointment)
            db.session.commit()

            user_details = User_Details.query.filter_by(
                user_name=current_user.full_name).first()

            if not user_details:
                flash("User details not found. Please update your profile.", "danger")
                return redirect(url_for('core.index'))

            # user_a_email = provider.email
            # user_b_email = current_user.email
            # subject = "New Appointment Booking"

            # email_content_user_a = f"""
            # Hi {provider.full_name},

            # You have a new appointment request from {current_user.full_name} {current_user.email}, {user_details.phone_number}
            # for your service "{service.name}" on {form.date.data} from {form.start_time.data} to {form.end_time.data}.
            # Please log in to your dashboard to accept or decline this appointment.

            # Regards,
            # Your Service Team
            # """
            # email_content_user_b = f"""
            # Hi {current_user.full_name},

            # Your booking for the service "{service.name} {service.provider_name}" on {form.date.data} from {form.start_time.data} to {form.end_time.data} has been submitted.
            # You will be notified once the service provider confirms the appointment.

            # Regards,
            # Your Service Team
            # """

            # # try:
            # #     send_mail(user_a_email, subject, email_content_user_a)
            # #     send_mail(user_b_email, subject, email_content_user_b)
            # # except Exception as email_error:
            # #     flash(f"An error occurred while sending emails: {
            # #           str(email_error)}", 'danger')

            notification_user_a = Notification(
                user_name=provider.full_name,
                message=f"You have a new appointment request from {current_user.full_name}, ({current_user.email}, {user_details.phone_number}) for service '{service.name}' on {form.date.data}.", read=False
            )
            notification_user_b = Notification(
                user_name=current_user.full_name,
                message=f"Your booking request for service '{service.name}' on {form.date.data} has been submitted and is awaiting confirmation from {provider.full_name}.", read=False
            )

            db.session.add(notification_user_a)
            db.session.add(notification_user_b)
            db.session.commit()

            flash('Your booking request has been submitted, check your Inbox', 'success')
            return redirect(url_for('core.index'))

        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {str(e)}", 'danger')

    return render_template('book_service.html', service=service, provider=provider, provider_details=provider_details, form=form)


@booking_system.route('/accept/appointment/<int:appointment_id>', methods=['GET', 'POST'])
@csrf.exempt
@login_required
def accept(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)

    if appointment.service_name not in [service.name for service in current_user.services]:
        flash("You do not have permission to accept this appointment", "danger")
        return redirect(url_for('core.index'))

    if appointment.status in ['Confirmed', 'Declined']:
        flash(f"This appointment has already been {appointment.status.lower()}.", "info")
        return redirect(url_for('core.index'))
    


    if request.method == 'POST':
        appointment.status = 'Confirmed'
        db.session.commit()

        user_b = User.query.filter_by(full_name=appointment.user_name).first()
        if user_b:
            # subject = "Appointment Accepted"
            # email_content = f"""
            # Hi {user_b.full_name},

            # Your appointment for the service "{appointment.service_name}" on {appointment.date} has been accepted.

            # Regards,
            # Your Service Team
            # """
            # send_mail(user_b.email, subject, email_content)

            notification_user_b = Notification(
                user_name=user_b.full_name,
                message=f"Your appointment for service '{appointment.service_name}' on {appointment.date} has been accepted.", read=False)
            db.session.add(notification_user_b)
            db.session.commit()

            flash("Appointment accepted successfully!", "success")
        else:
            flash("User not found.", "danger")

        return redirect(url_for('core.index'))

    return render_template('accept_appointment.html', appointment=appointment)


@booking_system.route('/decline/appointment/<int:appointment_id>', methods=['GET', 'POST'])
@csrf.exempt
@login_required
def decline_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)

    if appointment.service_name not in [service.name for service in current_user.services]:
        flash("You do not have permission to decline this appointment", "danger")
        return redirect(url_for('core.index'))

    if appointment.status in ['Confirmed', 'Declined']:
        flash(f"This appointment has already been {appointment.status.lower()}.", "info")
        return redirect(url_for('core.index'))

    if request.method == 'POST':
        appointment.status = 'Declined'
        db.session.commit()

        user_b = User.query.filter_by(full_name=appointment.user_name).first()
        if user_b:
            # subject = "Appointment Declined"
            # email_content = f"""
            # Hi {user_b.full_name},

            # Your appointment for the service "{appointment.service_name}" on {appointment.date} has been declined.

            # Regards,
            # Your Service Team
            # """
            # send_mail(user_b.email, subject, email_content)

            notification_user_b = Notification(
                user_name=user_b.full_name,
                message=f"Your appointment for service '{appointment.service_name}' on {appointment.date} has been declined.", read=False )
            db.session.add(notification_user_b)
            db.session.commit()

            flash("Appointment declined successfully!", "success")
        else:
            flash("User not found.", "danger")

        return redirect(url_for('core.index'))

    return render_template('decline_appointment.html', appointment=appointment)


@booking_system.route('/cancel_appointment/<int:appointment_id>', methods=['POST'])
@login_required
def cancel_appointment(appointment_id):
    if current_user.role != 'customer':
        flash('Only customers can cancel appointments.')
        return redirect(url_for('core.index'))
    appointment = Appointment.query.get_or_404(appointment_id)

    if appointment.user_name != current_user.full_name:
        flash("You do not have permission to cancel this appointment", "danger")
        return redirect(url_for('core.index'))

    if appointment.status == 'Pending':
        db.session.delete(appointment)
        db.session.commit()

        service = Service.query.filter_by(
            name=appointment.service_name).first()
        if service:
            provider = User.query.filter_by(
                full_name=service.provider_name).first()
            if provider:
                # subject = "Appointment Cancelled"
                # email_content = f"""
                # Hi {provider.full_name},

                # The appointment for the service "{appointment.service_name}" on {appointment.date} has been cancelled by the user.

                # Regards,
                # Your Service Team
                # """
                # send_mail(provider.email, subject, email_content)

                flash("Appointment cancelled successfully!", "success")
            else:
                flash("Service provider not found.", "danger")
        else:
            flash("Service not found.", "danger")
    else:
        flash("You cannot cancel an appointment that has been confirmed.", "danger")

    return render_template('cancel.html', appointement=appointment)


@booking_system.route('/view/bookings', methods=['GET'])
@login_required
def view_bookings():
    if current_user.role != 'provider':
        flash('Only providers can view these bookings.')
        return redirect(url_for('core.index'))

    services = Service.query.filter_by(
        provider_name=current_user.full_name).all()

    confirmed_appointments = Appointment.query.filter(Appointment.service_name.in_(
        [service.name for service in services]), Appointment.status == 'Confirmed').all()

    declined_appointments = Appointment.query.filter(Appointment.service.name.in_(
        [service.name for service in services]), Appointment.status == 'Declined').all()

    confirmed_user_details = []
    for appointment in confirmed_appointments:
        user = User.query.filter_by(full_name=appointment.user_name).first()
        user_info = {
            'appointment_id': appointment.id,
            'full_name': user.full_name,
            'email': user.email,
            'username': user.username,
            'country': appointment.country,
            'state': appointment.state,
            'date': appointment.date,
            'start_time': appointment.start_time,
            'end_time': appointment.end_time,
            'status': appointment.status
        }
        confirmed_user_details.append(user_info)

    declined_user_details = []
    for appointment in declined_appointments:
        user = User.query.filter_by(full_name=appointment.user_name).first()
        user_info = {
            'appointment_id': appointment.id,
            'full_name': user.full_name,
            'email': user.email,
            'username': user.username,
            'country': appointment.country,
            'state': appointment.state,
            'date': appointment.date,
            'start_time': appointment.start_time,
            'end_time': appointment.end_time,
            'status': appointment.status
        }
        declined_user_details.append(user_info)

    return render_template('view_bookings.html', confirmed_user_details=confirmed_user_details, declined_user_details=declined_user_details)


@booking_system.route('/admin/cancel_booking/<user_name>/<service_name>', methods=['POST'])
@login_required
def cancel_booking(user_name, service_name):
    if current_user.role != 'admin':
        flash("You do not have permission to access this page.")
        return redirect(url_for('core.index'))

    booking = Appointment.query.filter_by(
        user_name=user_name, service_name=service_name).first()
    if booking:
        booking.status = 'Cancelled'
        db.session.commit()
        flash(f"Booking for {booking.user_name} with service {booking.service_name} has been cancelled.")
    else:
        flash("Booking not found.")

    return redirect(url_for('bookings.view_all_bookings'))


@booking_system.route('/admin/supsend/user/<user_name>', methods=['POST'])
@csrf.exempt
@login_required
def suspend_user(user_name):
    if current_user.role != 'admin':
        flash("You do not have permission to access this page.")
        return redirect(url_for('core.index'))
    user = User.query.filter_by(full_name=user_name).first()
    if user:
        user.is_active = False
        db.session.commit()
        flash(f'{user.full_name} has been suspended')
    else:
        flash('User not fund')
    return redirect(url_for('booking_system.view_all_users'))


@booking_system.route('/admin/reactivate/user/<user_name>/', methods=['POST'])
@csrf.exempt
@login_required
def reactivate_user(user_name):
    if current_user.role != 'admin':
        flash("You do not have permission to access this page.")
        return redirect(url_for('core.index'))
    user = User.query.filter_by(full_name=user_name).first()
    if user:
        user.is_active = True
        db.session.commit()
        flash(f"{user.full_name} has been reactivated")
    else:
        flash('User not found')
    return redirect(url_for('booking_system.view_all_users'))



@booking_system.route('/admin/delete/user/<user_name>', methods=['POST'])
@csrf.exempt
@login_required
def delete_user(user_name):
    if current_user.role != 'admin':
        flash("You do not have permission to access this page.", "danger")
        return redirect(url_for('core.index'))
    
    user = User.query.filter_by(full_name=user_name).first()
    
    if user:
        try:
            # Delete the user
            db.session.delete(user)
            db.session.commit()
            flash(f"User {user.full_name} has been deleted.", "success")
        except IntegrityError:
            db.session.rollback()
            flash("An error occurred while deleting the user. Integrity constraint failed.", "danger")
    else:
        flash("User not found.", "warning")
    
    return redirect(url_for('booking_system.view_all_users'))



@booking_system.route('/admin/view_all_users', methods=['GET'])
@login_required
def view_all_users():
    if current_user.role != 'admin':
        flash("You do not have permission to access this page.")
        return redirect(url_for('core.index'))

    users = User.query.all()
    return render_template('view_all_users.html', users=users)


@booking_system.route('/admin/view_providers', methods=['GET'])
@login_required
def view_providers():
    if current_user.role != 'admin':
        flash("You do not have permission to access this page.")
        return redirect(url_for('core.index'))

    providers = User.query.filter_by(role='provider').all()
    return render_template('view_providers.html', providers=providers)


@booking_system.route('/admin/view_customers', methods=['GET'])
@login_required
def view_customers():
    if current_user.role != 'admin':
        flash("You do not have permission to access this page.")
        return redirect(url_for('core.index'))

    customers = User.query.filter_by(role='customer').all()
    return render_template('view_customers.html', customers=customers)


@booking_system.route('/admin/view_all_services', methods=['GET'])
@login_required
def view_all_services():
    if current_user.role != 'admin':
        flash("You do not have permission to access this page.")
        return redirect(url_for('core.index'))

    users = Service.query.all()
    return render_template('view_all_services.html', users=users)


@booking_system.route('/admin/view_all_appointments', methods=['GET'])
@login_required
def view_all_appointments():
    # if current_user.role != 'admin':
    #     flash("You do not have permission to access this page.")
    #     return redirect(url_for('core.index'))

    users = Appointment.query.all()
    return render_template('view_all_appointments.html', users=users)


@booking_system.route('/admin/view_all_notifications', methods=['GET'])
@login_required
def view_all_notifications():
    # if current_user.role != 'admin':
    #     flash("You do not have permission to access this page.")
    #     return redirect(url_for('core.index'))

    notifications = db.session.query(
        Notification, User.full_name).join(User).all()

    return render_template('view_all_notifications.html', notifications=notifications)


@booking_system.route('/admin/notification/<int:notification_id>', methods=['GET'])
@login_required
def view_notification(notification_id):
    # if current_user.role != 'admin':
    #     flash("You do not have permission to access this page.")
    #     return redirect(url_for('core.index'))

    notification, user_name = db.session.query(Notification, User.full_name).join(
        User).filter(Notification.id == notification_id).first_or_404()
    if not notification.read:
        notification.read = True
        db.session.commit()
        # return jsonify({"success": True}), 200

    return render_template('view_notification.html', notification=notification, user_name=user_name)


@booking_system.route('/admin/delete_service/<service_name>', methods=['POST'])
@csrf.exempt
@login_required
def delete_services(service_name):
    # if current_user.role != 'admin':
    #     flash("You do not have permission to delete services.", "danger")
    #     return redirect(url_for('core.index'))

    service = Service.query.filter_by(name=service_name).first()
    if service:
        db.session.delete(service)
        db.session.commit()
        flash(f"Service {service.name} has been deleted.")
    else:
        flash("Service not found.")

    return redirect(url_for('booking_system.view_all_services'))


@booking_system.route('/provider/delete_service/<service_name>', methods=['POST'])
@csrf.exempt
@login_required
def delete_service(service_name):
    if current_user.role != 'provider':
        flash("You do not have permission to delete services.", "danger")
        return redirect(url_for('core.index'))

    service = Service.query.filter_by(name=service_name).first()

    if service and service.provider_name == current_user.full_name:
        db.session.delete(service)
        db.session.commit()
        flash(f"Service '{service.name}' has been deleted.", "success")
    else:
        flash("Service not found or you do not have permission to delete this service.", "danger")

    return redirect(url_for('core.index'))


@booking_system.route('/provider/services', methods=['GET'])
@login_required
def view_provider_services():
    if current_user.role != 'provider':
        flash("You do not have permission to view this page.", "danger")
        return redirect(url_for('core.index'))

    services = Service.query.filter_by(
        provider_name=current_user.full_name).all()

    return render_template('view_provider_services.html', services=services)


@booking_system.route('/service/<service_name>/review', methods=['GET', 'POST'])
@login_required
def add_review(service_name):
    service = Service.query.filter_by(name=service_name).first()
    if service:
        if request.method == 'POST':
            rating = request.form.get('rating')
            comment = request.form.get('comment')
            if not rating or not rating.isdigit() or int(rating) < 1 or int(rating) > 5:
                flash("Invalid rating. Please enter a number between 1 and 5.")
                return redirect(request.url)
            review = Review(
                service_name=service.name,
                reviewer_name=current_user.full_name,
                rating=int(rating),
                comment=comment
            )

            db.session.add(review)
            db.session.commit()
            flash('Your review has been submitted!', 'success')
            return redirect(url_for('booking_system.service_details', service_name=service_name))
        elif not service:
            flash('Service not found!', 'danger')
            return redirect(url_for('core.index'))
    return render_template('add_review.html', service=service)


@booking_system.route('/service/<service_name>/reviews', methods=['GET'])
@login_required
def reviews(service_name):
    service = Service.query.filter_by(name=service_name).first()
    if not service:
        flash('Service not found', 'danger')
        return redirect(url_for('core.index'))
    reviews = Review.query.filter_by(service_name=service_name).all()
    return render_template('reviews.html', reviews=reviews, service=service)

# //////////////////////////////
# ////////////////////////


@booking_system.route('/notifications', methods=['GET'])
@login_required
def user_notification():
    # Fetch all notifications for the current user, ordered by timestamp
    notifications = Notification.query.filter_by(
        user_name=current_user.full_name).order_by(Notification.timestamp.desc()).all()

    return render_template('notification.html', notifications=notifications)


@booking_system.route('/notification/<int:notification_id>', methods=['GET'])
@login_required
def user_notifications(notification_id):
    notification = Notification.query.filter_by(
        id=notification_id, user_name=current_user.full_name).first_or_404()

    if not notification.read:
        notification.read = True
        db.session.commit()

    return render_template('notifications_details.html', notification=notification)


@booking_system.route('/appointments', methods=['GET'])
@login_required
def appointments():
    appointments = Appointment.query.filter(Appointment.service_name.in_(
        [service.name for service in current_user.services])).all()

    return render_template('appointments.html', appointments=appointments)


@booking_system.route('/provider/complaint', methods=['GET', 'POST'])
@login_required
@csrf.exempt
def provider_complaint():
    if current_user.role != 'provider':
        flash('Only providers can send complaints.', 'danger')
        return redirect(url_for('core.index'))

    form = ComplaintForm()
    if form.validate_on_submit():
        complaint = Complaint(
            provider_name=current_user.full_name,
            provider_id=current_user.id,
            subject=form.subject.data,
            message=form.message.data
        )
        db.session.add(complaint)
        db.session.commit()
        flash('Complaint submitted successfully!', 'success')
        return redirect(url_for('core.index'))

    return render_template('provider_complaint.html', form=form)


@booking_system.route('/admin/provider_complaints', methods=['GET'])
@login_required
def view_provider_complaints():
    if current_user.role != 'admin':
        flash('Access restricted to admins.', 'danger')
        return redirect(url_for('core.index'))

    complaints = Complaint.query.filter(Complaint.status == "Pending", Complaint.provider_id.isnot(
        None)).order_by(Complaint.timestamp.desc()).all()

    return render_template('admin_provider_complaints.html', complaints=complaints)


@booking_system.route('/admin/provider_respond/<int:complaint_id>', methods=['GET', 'POST'])
@login_required
@csrf.exempt
def respond_provider_complaint(complaint_id):
    if current_user.role != 'admin':
        flash('Access restricted to admins.', 'danger')
        return redirect(url_for('core.index'))

    complaint = Complaint.query.get_or_404(complaint_id)

    if request.method == 'POST':
        response = request.form.get('response')
        if response:
            complaint.response = response
            complaint.status = 'Resolved'
            complaint.admin_name = current_user.full_name
            complaint.admin_id = current_user.id
            db.session.commit()
            flash('Response sent successfully!', 'success')
            return redirect(url_for('view_provider_complaints'))
        else:
            flash('Response cannot be empty.', 'danger')

    return render_template('respond_provider_complaint.html', complaint=complaint)


@booking_system.route('/customer/complaint', methods=['GET', 'POST'])
@login_required
@csrf.exempt
def customer_complaint():
    if current_user.role != 'customer':
        flash('Only customers can send complaints.', 'danger')
        return redirect(url_for('core.index'))

    form = ComplaintForm()
    if form.validate_on_submit():
        complaint = Complaint(
            customer_name=current_user.full_name,
            customer_id=current_user.id,
            subject=form.subject.data,
            message=form.message.data
        )
        db.session.add(complaint)
        db.session.commit()
        flash('Complaint submitted successfully!', 'success')
        return redirect(url_for('core.index'))

    return render_template('customer_complaint.html', form=form)


@booking_system.route('/admin/complaints', methods=['GET'])
# @csrf.exempt
@login_required
def view_complaints():
    if current_user.role != 'admin':
        flash('Access restricted to admins.', 'danger')
        return redirect(url_for('core.index'))

    complaints = Complaint.query.filter_by(
        status="Pending").order_by(Complaint.timestamp.desc()).all()
    return render_template('admin_complaints.html', complaints=complaints)


@booking_system.route('/admin/respond/<int:complaint_id>', methods=['GET', 'POST'])
@login_required
@csrf.exempt
def respond_complaint(complaint_id):
    if current_user.role != 'admin':
        flash('Access restricted to admins.', 'danger')
        return redirect(url_for('core.index'))

    complaint = Complaint.query.get_or_404(complaint_id)

    if request.method == 'POST':
        response = request.form.get('response')
        if response:
            complaint.response = response
            complaint.status = 'Resolved'
            complaint.admin_name = current_user.full_name
            complaint.admin_id = current_user.id
            db.session.commit()
            flash('Response sent successfully!', 'success')
            return redirect(url_for('booking_system.view_complaints'))
        else:
            flash('Response cannot be empty.', 'danger')

    return render_template('respond_complaint.html', complaint=complaint)
