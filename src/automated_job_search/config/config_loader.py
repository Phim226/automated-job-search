import json
from typing import Any
from automated_job_search.config.job import Job, Jobsite
from automated_job_search.definitions import JOB_DATA_DIR

class ConfigLoader:

    def __init__(self) -> None:
        with open(JOB_DATA_DIR/"job_sites.json", "r") as file:
            jobsites =  json.load(file)

        self._jobsites = dict()
        for site in jobsites:
            self._jobsites[site["scraper"]] = (Jobsite(**site))

        with open(JOB_DATA_DIR/"disqualification.json") as file:
            self._disqualifications: dict[str, list[str]] = json.load(file)

        with open(JOB_DATA_DIR/"scoring.json") as file:
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

    def load_space_careers_job(self, job_json: dict[str, Any]) -> Job:
        return Job(
                job_id = job_json["id"].lower(),
                title = job_json["title"].lower(),
                company = job_json["employer"]["name"].lower(),
                city = job_json["city"].lower(),
                country = job_json["country_display"].lower(),
                score = 0,
            )