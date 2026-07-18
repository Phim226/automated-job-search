import requests
from typing import Any
from automated_job_search.config.job import Jobsite

class Scraper:

    def __init__(self, job_sites: dict[str, Jobsite]) -> None:
        self._jobsites = job_sites

    def get_jobs(self) -> list[dict[str, Any]]:
        jobs = []
        jobs += self.retrieve_spacecareers_jobs()
        return jobs

    def retrieve_spacecareers_jobs(self) -> list[dict[str, Any]]:
        api = self._jobsites["space_careers"].api

        response = requests.get(api, timeout = 60)
        response.raise_for_status()
        total_jobs = response.json()["count"]

        response = requests.get(
            api, timeout = 60, params = {"include_expired": "false", "limit": total_jobs, "offset": 0}
        )
        response.raise_for_status()

        results: list[dict[str, Any]] = response.json()["results"]
        for result in results:
            result["job_site"] = self._jobsites["space_careers"].name

        return results

    def retrieve_spacecareers_job_details(self, job_ids: list[str]) -> list[dict[str, Any]]:
        api = self._jobsites["space_careers"].api
        details = []
        for id in job_ids:
            url = f"{api}{id}/"

            response = requests.get(url, timeout = 60)
            response.raise_for_status()

            details.append(response.json())

        return details
