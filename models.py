from typing import TypedDict


class Movie(TypedDict):
    title: str
    year: int
    rating: float
    poster_url: str
    note: str
    country: str