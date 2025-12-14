"""
SQLAlchemy ORM models for the AirportSearch project.

This module defines the database schema and relationships for:
- Airports
- Runways
- Navaids
- Frequencies
- Countries, Regions, and Airport types
- API keys used for authentication

These models are used by:
- FastAPI endpoints
- Alembic migrations
- Pydantic schemas (ORM mode)
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    Text,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# Base class for all ORM models
Base = declarative_base()


class AirportType(Base):
    """
    Reference table for airport types (e.g. large_airport, heliport).

    One airport type can be associated with multiple airports.
    """

    __tablename__ = "airport_types"

    code = Column(String, primary_key=True)
    description = Column(String)

    # One-to-many relationship with Airport
    airports = relationship("Airport", back_populates="airport_type")


class APIKey(Base):
    """
    Stores API keys used for authenticating external clients.

    Keys can be activated/deactivated without deletion.
    """

    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(Text, unique=True, nullable=False)
    is_active = Column(Boolean, default=True)


class Country(Base):
    """
    Reference table for countries.

    Linked to airports via ISO country code.
    """

    __tablename__ = "countries"

    id = Column(Integer)
    code = Column(String(50), primary_key=True)
    name = Column(String(50))
    continent = Column(String(50))
    wikipedia_link = Column(String(128))
    keywords = Column(String(64))

    airports = relationship("Airport", back_populates="country")


class NavidType(Base):
    """
    Reference table for navaid types (e.g. VOR, NDB, ILS).
    """

    __tablename__ = "navid_types"

    code = Column(String, primary_key=True)
    description = Column(String)

    # One-to-many relationship with Navaid
    navaid = relationship("Navaid", back_populates="navaid_type")


class Region(Base):
    """
    Reference table for regions (ISO 3166-2).
    """

    __tablename__ = "regions"

    id = Column(Integer)
    code = Column(String(150), primary_key=True)
    local_code = Column(String(150))
    name = Column(String(150))
    continent = Column(String(150))
    iso_country = Column(String(150))
    wikipedia_link = Column(String(150))
    keywords = Column(String(150))

    airports = relationship("Airport", back_populates="region")


class Frequency(Base):
    """
    Stores radio frequencies associated with an airport
    (ATIS, Tower, Ground, etc.).
    """

    __tablename__ = "frequencies"

    id = Column(Integer, primary_key=True)
    airport_ref = Column(Integer)
    airport_ident = Column(String(150), ForeignKey("airports.ident"))
    type = Column(String(150))
    description = Column(String(150))
    frequency_mhz = Column(Float)

    # Relationship resolved via airport_ident
    airport = relationship(
        "Airport",
        primaryjoin="foreign(Frequency.airport_ident) == Airport.ident",
        back_populates="frequencies",
    )


class Navaid(Base):
    """
    Stores navigation aids (VOR, NDB, ILS, etc.).

    Some navaids are associated with an airport via ICAO ident.
    """

    __tablename__ = "navaids"

    id = Column(Integer, primary_key=True)
    filename = Column(String(50))
    ident = Column(String(50))
    name = Column(String(50))
    type = Column(String(50), ForeignKey("navid_types.code"))
    frequency_khz = Column(Integer)
    latitude_deg = Column(Float)
    longitude_deg = Column(Float)
    elevation_ft = Column(Integer)
    iso_country = Column(String(50))
    dme_frequency_khz = Column(Integer)
    dme_channel = Column(String(50))
    dme_latitude_deg = Column(Float)
    dme_longitude_deg = Column(Float)
    dme_elevation_ft = Column(Integer)
    slaved_variation_deg = Column(String(50))
    magnetic_variation_deg = Column(Float)
    usagetype = Column(String(50))
    power = Column(String(50))
    associated_airport = Column(String(50))

    # Relationships
    navaid_type = relationship("NavidType", back_populates="navaid")

    airport = relationship(
        "Airport",
        primaryjoin="foreign(Navaid.associated_airport) == Airport.ident",
        back_populates="navaids",
    )


class Runway(Base):
    """
    Stores runway information for an airport.
    """

    __tablename__ = "runways"

    id = Column(Integer, primary_key=True)
    airport_ref = Column(Integer)
    airport_ident = Column(String(150), ForeignKey("airports.ident"))
    length_ft = Column(Integer)
    width_ft = Column(Integer)
    surface = Column(String(150))
    lighted = Column(Integer)
    closed = Column(Integer)

    # Low end (LE)
    le_ident = Column(String(150))
    le_latitude_deg = Column(Float)
    le_longitude_deg = Column(Float)
    le_elevation_ft = Column(Integer)
    le_heading_degt = Column(Integer)
    le_displaced_threshold_ft = Column(Integer)

    # High end (HE)
    he_ident = Column(String(150))
    he_latitude_deg = Column(Float)
    he_longitude_deg = Column(Float)
    he_elevation_ft = Column(Integer)
    he_heading_degt = Column(Integer)
    he_displaced_threshold_ft = Column(Integer)

    airport = relationship(
        "Airport",
        primaryjoin="foreign(Runway.airport_ident) == Airport.ident",
        back_populates="runways",
    )


class Airport(Base):
    """
    Core airport entity.

    Acts as the central aggregation point for:
    - Frequencies
    - Runways
    - Navaids
    - Country, region, and airport type
    """

    __tablename__ = "airports"

    id = Column(Integer)
    ident = Column(String(150), primary_key=True)
    type = Column(String(150), ForeignKey("airport_types.code"))
    name = Column(String(250))
    latitude_deg = Column(Float)
    longitude_deg = Column(Float)
    elevation_ft = Column(Integer)
    continent = Column(String(150))
    iso_country = Column(String(150), ForeignKey("countries.code"))
    iso_region = Column(String(150), ForeignKey("regions.code"))
    municipality = Column(String(250))
    scheduled_service = Column(String(150))
    gps_code = Column(String(150))
    iata_code = Column(String(150))
    local_code = Column(String(150))
    home_link = Column(String(350))
    wikipedia_link = Column(String(350))
    keywords = Column(String(350))

    # Relationships
    airport_type = relationship("AirportType", back_populates="airports")
    country = relationship("Country", back_populates="airports")
    region = relationship("Region", back_populates="airports")

    frequencies = relationship("Frequency", back_populates="airport")
    runways = relationship("Runway", back_populates="airport")

    navaids = relationship(
        "Navaid",
        primaryjoin="Airport.ident == foreign(Navaid.associated_airport)",
        back_populates="airport",
        lazy="joined",  # Eager load for API performance
    )