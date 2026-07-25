"""
Shared pytest fixtures and configuration.

Provides an in-memory SQLite database for fast, isolated unit tests
that don't require a live MySQL instance.

Spec reference: §40 Test Infrastructure
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import get_db
from app.main import app


# ─── In-Memory SQLite Engine ─────────────────────────

SQLALCHEMY_TEST_URL = "sqlite://"

test_engine = create_engine(
    SQLALCHEMY_TEST_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)


# ─── Fixtures ────────────────────────────────────────


@pytest.fixture(scope="session", autouse=True)
def create_tables():
    """Create all tables once per test session."""
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture()
def db_session() -> Session:
    """Provide a transactional DB session that rolls back after each test.

    This ensures full test isolation — no test can pollute another.
    """
    connection = test_engine.connect()
    transaction = connection.begin()
    session = TestSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def client(db_session: Session) -> TestClient:
    """Provide a FastAPI TestClient wired to the test DB session.

    Overrides the `get_db` dependency so API tests hit SQLite
    instead of the real MySQL database.
    """

    def _override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as tc:
        yield tc
    app.dependency_overrides.clear()


# ─── Helper Factories ────────────────────────────────


@pytest.fixture()
def sample_policy_data() -> dict:
    """Return a valid PolicyCreate-compatible dict for tests."""
    return {
        "name": "Test Policy",
        "description": "A test policy for unit tests",
        "domain": "telecom",
        "priority": 100,
        "decision": "APPROVE",
        "conditions": {
            "all": [
                {
                    "field": "customer.credit_score",
                    "operator": "greater_than",
                    "value": 600,
                }
            ]
        },
        "reason": "Credit score above threshold",
    }


@pytest.fixture()
def sample_evaluation_request() -> dict:
    """Return a valid EvaluationRequest-compatible dict for tests."""
    return {
        "domain": "telecom",
        "customer_id": "cust_test_001",
        "data": {
            "customer.credit_score": 750,
            "customer.payment_history_defaults": 0,
            "customer.tenure_months": 24,
            "customer.plan_type": "premium",
            "account.outstanding_balance": 0,
            "account.status": "current",
        },
    }
