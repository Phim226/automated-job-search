from dataclasses import dataclass

@dataclass
class Job:
    title: str
    company: str
    city: str
    country: str
    score: int

    def __str__(self) -> str:
        return f"Job(Title = {self.title}, Company = {self.company}, Score = {self.score})"

@dataclass
class JobDetails(Job):
    duration: str
    deadline: str
    rolling_deadline: bool
    on_site_remote: str
    description: str
    application_url: str
    advert_url: str



@dataclass
class Jobsite:
    name: str
    url: str
    api: str
    scraper: str