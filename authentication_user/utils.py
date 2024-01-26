from django.core.mail import EmailMessage
import os


def send_email(data):
    email = EmailMessage(
      subject=data['subject'],
      body=data['body'],
      from_email=os.environ.get('EMAIL_FROM'),
      to=[data['to_email']]
    )
    email.send()

# from celery import Celery

# app = Celery('app', broker='redis://127.0.0.1:6379')

# @app.task
# def add(x, y):
#     return x + y