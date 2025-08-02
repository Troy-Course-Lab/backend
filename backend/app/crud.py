from sqlmodel import Session, select
import re

from app.core.security import get_password_hash, verify_password
from app.models import User
from app.schemas import UserCreate, UserUpdate


def get_user_by_email(*, session: Session, email: str) -> User | None:
    """
    Retrieve a user from the database based on their email address.
    """
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()


def create_user(*, session: Session, user_in: UserCreate) -> User:
    """
    Create a new user in the database.
    The password is automatically hashed before saving.
    """
    # Create a dictionary of the user data, excluding the password
    user_data = user_in.model_dump(exclude={"password"})
    
    if not user_data.get("id_troy"):
        if user_in.email.endswith("@troy.edu"):
            numbers = re.findall(r'\d+', user_in.email)
            if numbers:
                user_data["id_troy"] = numbers[0]
            else:
                # Generate a unique 6-digit ID
                import random
                while True:
                    id_troy = f"{random.randint(100000, 999999)}"
                    # Check if this ID already exists
                    existing_user = session.exec(select(User).where(User.id_troy == id_troy)).first()
                    if not existing_user:
                        user_data["id_troy"] = id_troy
                        break
        else:
            # Generate a unique 6-digit ID
            import random
            while True:
                id_troy = f"{random.randint(100000, 999999)}"
                # Check if this ID already exists
                existing_user = session.exec(select(User).where(User.id_troy == id_troy)).first()
                if not existing_user:
                    user_data["id_troy"] = id_troy
                    break
    
    # Hash the password and add it to the user data
    user_data["hashed_password"] = get_password_hash(user_in.password)
    
    db_user = User(**user_data)
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def update_user(*, session: Session, db_user: User, user_in: UserUpdate) -> User:
    """
    Update a user's details in the database.
    """
    user_data = user_in.model_dump(exclude_unset=True)
    if "password" in user_data and user_data["password"]:
        hashed_password = get_password_hash(user_data["password"])
        del user_data["password"]
        user_data["hashed_password"] = hashed_password
        
    for key, value in user_data.items():
        setattr(db_user, key, value)
        
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def authenticate(*, session: Session, email: str, password: str) -> User | None:
    """
    Authenticate a user by email and password.
    Returns the user object if authentication is successful, otherwise None.
    """
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user
