from pydantic import BaseModel, Field
from typing import Optional


class Movie(BaseModel):
    scheduled_date: Optional[str]
    scheduled_hour: str
    title: str
    language: str
    detail: str


class MovieByDate(BaseModel):
    scheduled_hour: str
    title: str
    language: str
    detail: str


class MovieDetail(BaseModel):
    genre: str
    release_date: str
    length: str
    synopsis: str
    trailer: str
