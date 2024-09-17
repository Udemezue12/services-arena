# import os
# import requests
# import logging
# from datetime import datetime
# from dotenv import load_dotenv
# from flask_bcrypt import generate_password_hash
# from flask import Flask, redirect, render_template, Blueprint, flash, url_for, request
# from sqlalchemy.exc import IntegrityError
# from flask_login import current_user, login_user, login_required
# from book.extensions import db, login_manager
# from book.fetch import fetch_country_choices, states
# from book.models import Service
# from users.forms import ServiceForm


# booking_system = Blueprint(__name__, 'booking_system')

# # //////////////////////////


# @booking_system.route('/create/service', methods=['GET', 'POST'])
# @login_required
# def create_service():
#     form = ServiceForm()
#     if request.method == 'POST':
#         selected_country = request.form.get('country')
#         form.state.choices = [(state, state)
#                               for state in states.get(selected_country, [])]
#         form.country.choices = fetch_country_choices()
#         if form.validate_on_submit():
#             service = Service(
#                 name=form.name.data,
#                 description=form.description.data,
#                 country=form.country.data,
#                 state=form.state.data,
#                 category=form.categoory.data,
#                 price=float(form.price.data),
#                 provider_name=current_user.full_name
#             )
#             db.session.add(service)
#             db.session.commit()
#             flash('Service created successfully', 'success')
#             return redirect(url_for('core.index'))
#         return render_template('create_service.html', form=form)
    
