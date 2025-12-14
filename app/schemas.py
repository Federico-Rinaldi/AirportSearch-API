"""
Pydantic schemas used for request validation and response serialization.

These schemas define the public contract of the AirportSearch API and are
used by FastAPI to:
- validate outgoing responses
- generate OpenAPI (Swagger) documentation
- serialize SQLAlchemy ORM models safely
"""

from typing import Optional, List
from pydantic import BaseModel


class AirportTypeSchema(BaseModel):
    """
    Represents the classification of an airport (e.g. large_airport, heliport).

    This schema is typically nested inside AirportSchema.
    """

    code: str
    description: Optional[str]

    class Config:
        # Enables compatibility with SQLAlchemy ORM objects
        orm_mode = True


class ApiKeySchema(BaseModel):
    """
    Public representation of an API key.

    Used for administrative endpoints or internal tooling.
    The actual key value should never be exposed publicly in production APIs.
    """

    id: int
    key: str
    is_active: Optional[bool] = True

    class Config:
        orm_mode = True


class CountrySchema(BaseModel):
    """
    Represents a country associated with an airport.
    """

    id: Optional[int]
    code: str
    name: Optional[str]
    continent: Optional[str]
    wikipedia_link: Optional[str]
    keywords: Optional[str]

    class Config:
        orm_mode = True


class NavidTypeSchema(BaseModel):
    """
    Represents the classification of a navigation aid (NAVAID),
    such as VOR, NDB, or ILS.
    """

    code: str
    description: Optional[str]

    class Config:
        orm_mode = True


class RegionSchema(BaseModel):
    """
    Represents an administrative or geographic region (e.g. US-CA, IT-62).
    """

    id: Optional[int]
    code: str
    local_code: Optional[str]
    name: Optional[str]
    continent: Optional[str]
    iso_country: Optional[str]
    wikipedia_link: Optional[str]
    keywords: Optional[str]

    class Config:
        orm_mode = True


class FrequencySchema(BaseModel):
    """
    Represents a radio frequency associated with an airport.

    Frequencies are used for air traffic control, ground operations,
    and communication between pilots and airport services.
    """

    id: Optional[int]
    airport_ref: Optional[int]
    airport_ident: Optional[str]
    type: Optional[str]
    description: Optional[str]
    frequency_mhz: Optional[float]

    class Config:
        orm_mode = True


class NavaidSchema(BaseModel):
    """
    Represents a navigation aid (NAVAID) used in aviation navigation.

    Includes both primary and DME-related attributes.
    """

    id: Optional[int]
    filename: Optional[str]
    ident: Optional[str]
    name: Optional[str]
    type: Optional[str]
    frequency_khz: Optional[int]
    latitude_deg: Optional[float]
    longitude_deg: Optional[float]
    elevation_ft: Optional[int]
    iso_country: Optional[str]
    dme_frequency_khz: Optional[int]
    dme_channel: Optional[str]
    dme_latitude_deg: Optional[float]
    dme_longitude_deg: Optional[float]
    dme_elevation_ft: Optional[int]
    slaved_variation_deg: Optional[str]
    magnetic_variation_deg: Optional[float]
    usagetype: Optional[str]
    power: Optional[str]
    associated_airport: Optional[str]

    class Config:
        orm_mode = True


class RunwaySchema(BaseModel):
    """
    Represents a runway belonging to an airport.

    Includes both low-end (LE) and high-end (HE) runway data.
    """

    id: Optional[int]
    airport_ref: Optional[int]
    airport_ident: Optional[str]
    length_ft: Optional[int]
    width_ft: Optional[int]
    surface: Optional[str]
    lighted: Optional[int]
    closed: Optional[int]

    le_ident: Optional[str]
    le_latitude_deg: Optional[float]
    le_longitude_deg: Optional[float]
    le_elevation_ft: Optional[int]
    le_heading_degt: Optional[int]
    le_displaced_threshold_ft: Optional[int]

    he_ident: Optional[str]
    he_latitude_deg: Optional[float]
    he_longitude_deg: Optional[float]
    he_elevation_ft: Optional[int]
    he_heading_degt: Optional[int]
    he_displaced_threshold_ft: Optional[int]

    class Config:
        orm_mode = True


class AirportSchema(BaseModel):
    """
    Main airport representation returned by the API.

    This schema aggregates all related entities such as:
    - country
    - region
    - runways
    - frequencies
    - navigation aids
    """

    id: Optional[int]
    ident: str
    type: Optional[str]
    name: Optional[str]
    latitude_deg: Optional[float]
    longitude_deg: Optional[float]
    elevation_ft: Optional[int]
    continent: Optional[str]
    iso_country: Optional[str]
    iso_region: Optional[str]
    municipality: Optional[str]
    scheduled_service: Optional[str]
    gps_code: Optional[str]
    iata_code: Optional[str]
    local_code: Optional[str]
    home_link: Optional[str]
    wikipedia_link: Optional[str]
    keywords: Optional[str]

    # Nested relational objects
    airport_type: Optional[AirportTypeSchema]
    country: Optional[CountrySchema]
    region: Optional[RegionSchema]

    # One-to-many relationships
    runways: List[RunwaySchema] = []
    frequencies: List[FrequencySchema] = []
    navaids: List[NavaidSchema] = []

    class Config:
        orm_mode = True