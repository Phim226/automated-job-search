from typing import Any
from automated_job_search.config.job import Job, JobDetails, Jobsite

class ConfigLoader:

    def __init__(self, job_sites: dict[str, Jobsite]) -> None:
        self._job_sites = job_sites

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