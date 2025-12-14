"""
Database connection and session management for the AirportSearch API.

This module is responsible for:
- Reading the database connection string from environment variables
- Creating the SQLAlchemy engine
- Providing a session factory for dependency injection
- Defining the shared Base class for ORM models

The DATABASE_URL is expected to be provided via environment variables,
especially when running inside Docker/Podman containers.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ---------------------------------------------------------------------------
# Database configuration
# ---------------------------------------------------------------------------

# Read the database connection string from the environment.
# Example:
# postgresql://username:password@hostname:5432/database_name
#
# NOTE:
# - Do NOT hardcode credentials in production.
# - The default value is intended for local development only.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://airportuser:password@db:5432/airportdb",
)

# ---------------------------------------------------------------------------
# SQLAlchemy engine
# ---------------------------------------------------------------------------

# Create the SQLAlchemy engine.
# pool_pre_ping helps avoid stale connections in long-running applications.
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

# ---------------------------------------------------------------------------
# Session factory
# ---------------------------------------------------------------------------

# SessionLocal is used by FastAPI dependencies to create
# one database session per request.
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

# ---------------------------------------------------------------------------
# Declarative base
# ---------------------------------------------------------------------------

# Base class for all ORM models.
# This must be imported by Alembic to enable autogeneration.
Base = declarative_base()