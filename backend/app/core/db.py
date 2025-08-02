from sqlmodel import Session, create_engine

from app.core.config import settings

# The database engine is created using the URI from the application settings.
engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


# This function is a stub and is not directly called for initial data creation.
# The primary initialization logic is triggered by the backend_pre_start.py script,
# which executes the logic defined in app/initial_data.py.
def init_db(session: Session) -> None:
    """
    This function is kept for structural consistency but does not perform
    the initial database setup.
    """
    pass
