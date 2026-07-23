from dataclasses import dataclass, fields

@dataclass
class IterableDataClass:

    def __iter__(self):
        return iter(tuple(getattr(self, field.name) for field in fields(self)))

    def __len__(self) -> int:
        return len(fields(self))

    def __getitem__(self, key):
        _fields = fields(self)

        if isinstance(key, slice):
            return tuple(getattr(self, field.name) for field in _fields[key])

        return getattr(self, fields(self)[key].name)

@dataclass
class Job(IterableDataClass):
    job_id: str
    title: str
    company: str
    city: str
    country: str
    job_site: str
    score: int

@dataclass
class JobDetails(Job):
    data_posted: str
    duration: str | None
    deadline: str | None
    rolling_deadline: bool
    salary_range_lower: str | None
    salary_range_upper: str | None
    expired: bool
    on_site_remote: str | None
    application_url: str
    advert_url: str
    description: str

@dataclass
class Jobsite(IterableDataClass):
    name: str
    url: str
    api: str