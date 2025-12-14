"""
Main FastAPI application module.

This module:
- Initializes the FastAPI application
- Configures global dependencies (API Key security)
- Sets up CORS middleware
- Exposes API endpoints for airport search

Security:
- All endpoints are protected via API Key authentication
- API keys are validated against the database
"""

from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    Security,
    status,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select

from . import models, schemas, database


# ---------------------------------------------------------------------------
# Database dependency
# ---------------------------------------------------------------------------

def get_db() -> Session:
    """
    Provide a SQLAlchemy database session.

    This dependency:
    - Creates a new database session per request
    - Ensures the session is always closed after use

    Yields:
        Session: SQLAlchemy database session
    """
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------------------------------------------------------
# API Key security
# ---------------------------------------------------------------------------

# Define API key header (x-api-key)
api_key_header = APIKeyHeader(
    name="x-api-key",
    auto_error=False,  # Disable automatic 403 to allow custom error handling
)


def verify_api_key(
    api_key: str = Security(api_key_header),
    db: Session = Depends(get_db),
) -> None:
    """
    Validate API Key provided in the request headers.

    This function:
    - Ensures the API key is present
    - Verifies that the key exists in the database
    - Checks that the key is active

    Raises:
        HTTPException: 401 if the API key is missing, invalid, or inactive
    """
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key",
        )

    # Look up the API key in the database
    db_key = (
        db.query(models.APIKey)
        .filter(
            models.APIKey.key == api_key,
            models.APIKey.is_active.is_(True),
        )
        .first()
    )

    if not db_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or inactive API key",
        )


# ---------------------------------------------------------------------------
# FastAPI application initialization
# ---------------------------------------------------------------------------

# Apply API key verification as a global dependency
app = FastAPI(
    title="Airport Search API",
    version="1.0.0",
    description="""
    AirportSearch provides a REST API to query airports, frequencies, navaids and runways.

    🔐 Access is protected via API Key authentication.
    📊 Rate limiting is enforced per API key.
    """,
    contact={
        "name": "Federico Rinaldi",
        "url": "https://federicorinaldi.dev/",
        "email": "fede@federicorinaldi.dev",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    dependencies=[Depends(verify_api_key)],
)


# ---------------------------------------------------------------------------
# CORS configuration
# ---------------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# API endpoints
# ---------------------------------------------------------------------------

@app.get(
    "/airportByName/{name}",
    response_model=list[schemas.AirportSchema],
)
def get_airports_by_name(
    name: str,
    db: Session = Depends(get_db),
):
    """
    Retrieve airports matching a given name or ident.

    The search:
    - Is case-insensitive
    - Matches both airport name and ident
    - Eager-loads related entities to avoid N+1 queries

    Args:
        name (str): Partial or full airport name or ICAO/IATA ident
        db (Session): Database session dependency

    Returns:
        list[AirportSchema]: List of matching airports

    Raises:
        HTTPException: 404 if no airports are found
    """
    like_pattern = f"%{name}%"

    result = db.execute(
        select(models.Airport)
        .options(
            joinedload(models.Airport.airport_type),
            joinedload(models.Airport.country),
            joinedload(models.Airport.region),
            joinedload(models.Airport.navaids),
        )
        .where(
            (models.Airport.name.ilike(like_pattern))
            | (models.Airport.ident.ilike(like_pattern))
        )
    )

    airports = result.unique().scalars().all()

    if not airports:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No airport found with that name or ident",
        )

    return airports