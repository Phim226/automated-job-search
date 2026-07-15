import json
from typing import Any
from automated_job_search.config.job import Job, JobDetails, Jobsite
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

    def load_space_careers_job(self, job_jsons: list[dict[str, Any]]) -> list[Job]:
        jobs = []
        for job in job_jsons:
            jobs.append(
                Job(
                    job_id = job["id"].lower(),
                    title = job["title"].lower(),
                    company = job["employer"]["name"].lower(),
                    city = job["city"].lower(),
                    country = job["country_display"].lower(),
                    job_site = job["job_site"],
                    score = 0,
                )
            )

        return jobs

    def load_job_from_db(self, job_db_entries: list[tuple[str, str, str, str, str, str, int]]) -> list[Job]:
        jobs = []
        for job in job_db_entries:
            jobs.append(Job(*job))

        return jobs

    def load_space_careers_job_details(self, job_info_pair: list[tuple[Job, dict[str, Any]]]) -> list[JobDetails]:
        job_details = []
        for job_summary, details in job_info_pair:
            job_details.append(
                JobDetails(
                    *job_summary,
                    data_posted= "",
                    duration = "",
                    deadline = "",
                    rolling_deadline = True,
                    expired = False,
                    on_site_remote = "",
                    description = "",
                    application_url = "",
                    advert_url = ""
                )
            )

        return job_details