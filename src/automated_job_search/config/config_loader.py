import json
from pathlib import Path
from typing import Any
from automated_job_search.config.job import Job, Jobsite

class ConfigLoader:

    def __init__(self) -> None:
        job_data_path = Path(__file__).resolve().parent.parent.parent.parent/"job_data"

        with open(job_data_path/"job_sites.json", "r") as file:
            jobsites =  json.load(file)

        self._jobsites = dict()
        for site in jobsites:
            self._jobsites[site["scraper"]] = (Jobsite(**site))

        with open(job_data_path/"disqualification.json") as file:
            self._disqualifications: dict[str, list[str]] = json.load(file)

        with open(job_data_path/"scoring.json") as file:
            self._scoring: dict[str, dict[str, int]] = json.load(file)

    @property
    def jobsites(self) -> dict[str, Jobsite]:
        return self._jobsites

    @property
    def disqualifications(self) -> dict[str, list[str]]:
        return self._disqualifications

    @property
    def scoring(self) -> dict[str, dict[str, int]]:
        return self._scoring

    def load_space_careers_job(self, job_json: dict[str, Any], advert_url: str, description: str) -> Job:
        return Job(
                title = job_json["title"].lower(),
                company = job_json["employer"]["name"].lower(),
                city = job_json["city"].lower(),
                country = job_json["country_display"].lower(),
                description = description.lower(),
                advert_url = advert_url
            )