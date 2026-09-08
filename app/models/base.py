from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """
    Clase base para todos los modelos SQLAlchemy 2.0.
    A partir de aquí heredarán global_entities, tenant_entities, etc.
    """
    pass