import requests
from typing import Any
from automated_job_search.config.job import Jobsite

class Scraper:

    def __init__(self, job_sites: dict[str, Jobsite]) -> None:
        self._jobsites = job_sites

    def get_jobs(self) -> list[dict[str, Any]]:
        jobs = []
        jobs += self.retrieve_spacecareers_jobs()
        # filtered_jobs = self.filter_jobs(spacecareers_jobs)
        return jobs

    def retrieve_spacecareers_jobs(self) -> list[dict[str, Any]]:
        api = self._jobsites["space_careers"].api

        response = requests.get(api)
        if not response.ok:
            print(f"Request to spacecareers.uk was not successful. Code {response.status_code}")
            return []

        total_jobs = response.json()["count"]
        api_request = f"{api}?include_expired=false&limit={total_jobs}&offset=0"

        response = requests.get(api_request)

        if not response.ok:
            print(f"Request to spacecareers.uk was not successful. Code {response.status_code}")
            return []

        #advert_url = f"{self._jobsites["space_careers"].url}{job["id"]}"
        results: list[dict[str, Any]] = response.json()["results"]
        for result in results:
            result["job_site"] = self._jobsites["space_careers"].scraper

        return results

    def get_space_careers_job_details(self, job_id: str) -> dict[str, Any]:
        api = self._jobsites["space_careers"].api
        url = f"{api}{job_id}/"

        response = requests.get(url)
        return response.json()
