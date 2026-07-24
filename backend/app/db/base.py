"""
SQLAlchemy Declarative Base.

All ORM models inherit from this base class.
Table names use snake_case.

Spec reference: §10 Database Base and Naming Convention
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models."""

    pass
