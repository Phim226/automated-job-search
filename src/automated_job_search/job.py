from dataclasses import dataclass

@dataclass
class Job:
    title: str
    company: str
    city: str
    country: str
    description: str= ""
    advert_url: str = ""
    score: int = 0

    def __str__(self) -> str:
        return f"Job(Title = {self.title}, Company = {self.company}, Score = {self.score})"

@dataclass
class Jobsite:
    name: str
    url: str
    api: str
    scraper: str