from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from celery.exceptions import MaxRetriesExceededError  # Correct import
import smtplib
import logging

logger = logging.getLogger(__name__)

@shared_task(
    autoretry_for=(smtplib.SMTPException,),  # Automatically retry on SMTP errors
    retry_backoff=True,                     # Use exponential backoff for retries
    retry_kwargs={'max_retries': 5}         # Limit to 5 retry attempts
)
def send_email_task(recipient, subject, message):
    """
    Celery task that sends an email asynchronously.
    Retries if email sending fails due to SMTPException.
    """
    try:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,  # From email (configured in settings.py)
            [recipient],               # Recipient email
            fail_silently=False,
        )
        logger.info(f"Email successfully sent to {recipient}")
        return f'Email sent to {recipient}'
    except smtplib.SMTPException as e:
        logger.warning(f"Retrying to send email to {recipient} due to: {e}")
        try:
            # Attempt to retry the task
            raise send_email_task.retry(exc=e)
        except MaxRetriesExceededError:
            # Log final failure if maximum retries are reached
            logger.error(f"Failed to send email to {recipient} after maximum retries.")
            return f"Failed to send email to {recipient} after maximum retries."
