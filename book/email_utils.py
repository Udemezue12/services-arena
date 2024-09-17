from flask_mail import Message
from book.extensions import mail
from flask import flash



def send_mail(recipient, subject, body):
    try:
        msg = Message(subject, recipients=[recipient])
        msg.body = body
        mail.send(msg)
    except Exception as e:
        flash(f"Failed to send email: {e}")