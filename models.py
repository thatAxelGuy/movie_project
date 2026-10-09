from typing import TypedDict


class Movie(TypedDict):
    title: str
    year: int
    rating: float
    poster_url: str
    country: str


class MovieWithNote(Movie):
    note: str