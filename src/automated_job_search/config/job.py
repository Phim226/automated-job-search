from dataclasses import dataclass, fields

@dataclass
class Job:
    job_id: str
    title: str
    company: str
    city: str
    country: str
    job_site: str
    score: int

    def __iter__(self):
        return iter(tuple(getattr(self, field.name) for field in fields(self)))

@dataclass
class JobDetails(Job):
    data_posted: str
    duration: str | None
    deadline: str | None
    rolling_deadline: bool
    expired: bool
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