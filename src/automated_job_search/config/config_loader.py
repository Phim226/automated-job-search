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
            duration: dict[Any, Any] | str | None = details["duration"]
            if duration is not None and isinstance(duration, dict):
                duration = ""
                for key, val in details["duration"].items():
                    if key == "permanent":
                        duration = key
                        break
                    else:
                        duration += f"{f"{val} {key}" if val != 0 else ""}"

            job_details.append(
                JobDetails(
                    *job_summary,
                    data_posted= details["posted_date"],
                    duration = duration,
                    deadline = details["application_deadline"],
                    rolling_deadline = details["rolling_deadline"],
                    salary_range_lower = details["salary_range_lower"],
                    salary_range_upper = details["salary_range_upper"],
                    expired = details["expired"],
                    on_site_remote = details["on_site_remote"].lower(),
                    description = details["description"],
                    application_url = details["link_to_application_form"],
                    advert_url = f"{self._job_sites["space_careers"].url}{job_summary.job_id}"
                )
            )

        return job_details