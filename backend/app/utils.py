import logging
from pathlib import Path
from typing import Any, Dict

import emails
from emails.template import JinjaTemplate

from app.core.config import settings


def send_email(
    email_to: str,
    subject_template: str = "",
    html_template: str = "",
    environment: Dict[str, Any] = {},
) -> None:
    """
    Sends an email using the configured SMTP server.
    """
    assert settings.emails_enabled, "Emailing is not enabled in the settings."
    message = emails.Message(
        subject=JinjaTemplate(subject_template),
        html=JinjaTemplate(html_template),
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
    )
    smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
    if settings.SMTP_TLS:
        smtp_options["tls"] = True
    if settings.SMTP_USER:
        smtp_options["user"] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        smtp_options["password"] = settings.SMTP_PASSWORD
    response = message.send(to=email_to, render=environment, smtp=smtp_options)
    logging.info(f"Send email result: {response}")


def generate_test_email(email_to: str) -> Dict[str, str]:
    """
    Generates test email data using the test_email template.
    """
    subject = f"{settings.PROJECT_NAME} - Test Email"
    
    # Read the test email HTML template
    template_path = Path(__file__).parent / "email-templates" / "src" / "test_email.html"
    with open(template_path) as f:
        html_template = f.read()
    
    return {
        "subject": subject,
        "html_content": html_template,
    }


def send_new_account_email(email_to: str, username: str, token: str) -> None:
    """
    Sends a verification email to a new user.
    """
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - New account verification"
    
    # Construct the verification link
    link = f"{settings.SERVER_HOST}/api/v1/verify-email?token={token}"
    
    template_path = Path(__file__).parent / "email-templates" / "src" / "new_account_verification.html"
    with open(template_path) as f:
        html_template = f.read()

    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=html_template,
        environment={
            "project_name": settings.PROJECT_NAME,
            "username": username,
            "email": email_to,
            "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            "link": link,
        },
    )
