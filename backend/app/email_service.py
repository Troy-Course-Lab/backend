import logging
from pathlib import Path
from typing import Any, Dict

import resend
from jinja2 import Template

from app.core.config import settings


class EmailService:
    def __init__(self):
        self.resend_api_key = settings.RESEND_API_KEY
        if self.resend_api_key:
            resend.api_key = self.resend_api_key
    
    def send_email(
        self,
        email_to: str,
        subject: str,
        html_content: str,
        from_email: str = None,
        from_name: str = None,
    ) -> bool:
        """
        Send email using Resend service.
        """
        if not self.resend_api_key:
            logging.warning("RESEND_API_KEY not configured, skipping email send")
            return False
        
        try:
            from_email = from_email or settings.EMAILS_FROM_EMAIL
            from_name = from_name or settings.EMAILS_FROM_NAME
            
            params = {
                "from": f"{from_name} <{from_email}>",
                "to": [email_to],
                "subject": subject,
                "html": html_content,
            }
            
            response = resend.Emails.send(params)
            logging.info(f"Email sent successfully: {response}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to send email: {e}")
            return False
    
    def send_verification_email(self, email_to: str, username: str, token: str) -> bool:
        """
        Send verification email to new user.
        """
        subject = f"{settings.PROJECT_NAME} - Verify Your Account"
        
        # Create verification link
        verification_url = f"{settings.SERVER_HOST}/api/v1/verify-email?token={token}"
        
        # Simple HTML template (you can enhance this)
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Verify Your Account</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #007bff;">Welcome to {settings.PROJECT_NAME}, {username}!</h2>
                
                <p>Thank you for registering. To complete your registration and verify your email address, please click the button below.</p>
                
                <p>This link is valid for {settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS} hours.</p>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{verification_url}" 
                       style="background-color: #007bff; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block;">
                        Verify Your Account
                    </a>
                </div>
                
                <p>If you did not create an account, no further action is required.</p>
                
                <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
                
                <p style="font-size: 14px; color: #666;">
                    If you're having trouble clicking the button, copy and paste the URL below into your web browser:
                </p>
                <p style="font-size: 14px; color: #666; word-break: break-all;">
                    <a href="{verification_url}">{verification_url}</a>
                </p>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(email_to, subject, html_content)
    
    def send_test_email(self, email_to: str) -> bool:
        """
        Send test email.
        """
        subject = f"{settings.PROJECT_NAME} - Test Email"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Test Email</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #007bff;">Test Email from {settings.PROJECT_NAME}</h2>
                
                <p>This is a test email to verify that the email service is working correctly.</p>
                
                <p>If you received this email, the email configuration is working properly!</p>
                
                <p style="font-size: 14px; color: #666;">
                    Sent to: {email_to}
                </p>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(email_to, subject, html_content)


# Global email service instance
email_service = EmailService() 