import requests
from typing import Any
from automated_job_search.config.job import Job
from automated_job_search.config.config_loader import ConfigLoader

class Scraper:

    def __init__(self, config_loader: ConfigLoader) -> None:
        self._config_loader = config_loader
        self._jobsites = config_loader.jobsites

    def get_jobs(self) -> list[dict[str, Any]]:
        jobs = []
        jobs += self.retrieve_spacecareers_jobs()
        # filtered_jobs = self.filter_jobs(spacecareers_jobs)
        return jobs

    def retrieve_spacecareers_jobs(self) -> list[dict[str, Any]]:
        api = self._jobsites["space_careers"].api

        total_jobs = requests.get(api).json()["count"]
        api_request = f"{api}include_expired=false&limit={total_jobs}&offset=0"

        response = requests.get(api_request)

        if not response.ok:
            print(f"Request to spacecareers.uk was not successful. Code {response.status_code}")
            return []

        #advert_url = f"{self._jobsites["space_careers"].url}{job["id"]}"
        results: list[dict[str, Any]] = response.json()["results"]
        for result in results:
            result["job_site"] = self._jobsites["space_careers"].name

        return results

    def _get_space_careers_job_details(self, job_id: str) -> dict[str, Any]:
        api = self._jobsites["space_careers"].api
        url = f"{api}{job_id}/"

        response = requests.get(url)
        return response.json()

    def filter_jobs(self, jobs_list: list[Job]) -> list[Job]:
        filtered_list = []
        job_disqualified = False
        for job in jobs_list:
            for title_disqualifer in self._config_loader.disqualifications["title"]:
                if title_disqualifer in job.title:
                    job_disqualified = True
                    break

            if job_disqualified:
                job_disqualified = False
                continue

            filtered_list.append(job)

        return filtered_list

    def apply_scoring(self, jobs_list: list[Job]) -> None:
        country_scores = self._config_loader.scoring["country"]
        city_scores = self._config_loader.scoring["city"]
        title_scores = self._config_loader.scoring["title"]

        for job in jobs_list:
            for country, score in country_scores.items():
                if country in job.country:
                    job.score += score

            for city, score in city_scores.items():
                if city in job.city:
                    job.score += score

            for title, score in title_scores.items():
                if title in job.title:
                    job.score += score


