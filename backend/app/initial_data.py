from sqlmodel import Session

from app import crud
from app.core.config import settings
from app.schemas import UserCreate
# This import is necessary for SQLModel to discover the User model
# before operations are performed on it.
from app.models import User


def init_db(session: Session) -> None:
    """
    Creates the first superuser (admin2) and admin1 user in the database if they do not exist.
    This function is called by the pre-start script.
    """
    # Check if the superuser (admin2) already exists.
    superuser = crud.get_user_by_email(session=session, email=settings.FIRST_SUPERUSER)
    
    # If the superuser does not exist, create them.
    if not superuser:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            id_troy="admin001",  # Provide a default Troy ID for the admin.
            name="Initial Superuser",  # Provide a default name.
            role="admin2",  # Set the role to the highest administrative level.
        )
        superuser = crud.create_user(session=session, user_in=user_in)
        
        # Manually set the first superuser as verified to bypass the email flow.
        superuser.is_verified = True
        session.add(superuser)
        session.commit()
    
    # Check if the admin1 user already exists.
    admin1_email = "admin1@example.com"
    admin1_user = crud.get_user_by_email(session=session, email=admin1_email)
    
    # If the admin1 user does not exist, create them.
    if not admin1_user:
        admin1_user_in = UserCreate(
            email=admin1_email,
            password="admin1password",  # Default password for admin1
            id_troy="admin002",  # Provide a default Troy ID for admin1.
            name="Admin 1 User",  # Provide a default name.
            role="admin1",  # Set the role to admin1 level.
        )
        admin1_user = crud.create_user(session=session, user_in=admin1_user_in)
        
        # Manually set the admin1 user as verified to bypass the email flow.
        admin1_user.is_verified = True
        session.add(admin1_user)
        session.commit()
