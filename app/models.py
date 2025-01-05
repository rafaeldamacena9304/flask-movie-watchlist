from dataclasses import dataclass, field

@dataclass
class Movie:
    _id: str
    cover: str
    title: str
    director: str
    genre: str
    subgenre: str
    description:str
    rating: float = 0.0
    num_ratings: int = 0
    comments: list[str] = field(default_factory=list)

    def add_rating(self, new_rating: float):
        if 1.0 <= new_rating <= 5.0:
            self.rating = (self.rating * self.num_ratings + new_rating) / (self.num_ratings + 1)
            self.num_ratings += 1
    
    def stars(self) -> int:
        return round(self.rating)


@dataclass
class User:
    _id: str
    name: str
    username: str
    password: str
    watched_movies: list[str] = field(default_factory=list)
    rated_movies: list[str] = field(default_factory=list)