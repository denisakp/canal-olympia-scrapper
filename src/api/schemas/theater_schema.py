from pydantic import BaseModel
from typing import List


class SocialNetwork(BaseModel):
    name: str | None = None
    href: str | None = None


class Pricing(BaseModel):
    name: str | None = None
    amount: str | None = None


class Schedule(BaseModel):
    day_slots: str | None = None
    time_slots: str | None = None


class Movie(BaseModel):
    movie_url: str | None = None
    movie_title: str | None = None
    session_hour: str | None = None
    language: str | None = None


class Session(BaseModel):
    scheduled_date: str | None = None
    weekday: str | None = None
    week_number: str | None = None
    movies: List[Movie] | None = []


class Theater(BaseModel):
    href: str | None = None
    name: str | None = None


class TheaterDetail(BaseModel):
    figure: str | None = None
    title: str | None = None
    address: str | None = None
    social_networks: List[SocialNetwork] | None = []
    pricing: List[Pricing] | None = []
    schedules: List[Schedule] | None = []
    sessions: List[Session] | None = []
