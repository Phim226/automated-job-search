import requests
from typing import Any
from job import Job
from config_loader import ConfigLoader
from playwright.sync_api import sync_playwright

class Scraper:

    def __init__(self, config_loader: ConfigLoader) -> None:
        self._config_loader = config_loader
        self._jobsites = config_loader.jobsites

    def get_jobs(self) -> list[Job]:
        spacecareers_jobs = self.retrieve_spacecareers_jobs()
        filtered_jobs = self.filter_jobs(spacecareers_jobs)
        return filtered_jobs

    def retrieve_spacecareers_jobs(self) -> list[Job]:
        site = self._jobsites["space_careers"]
        api = site.api

        total_jobs = requests.get(api).json()["count"]
        api_request = f"{api}include_expired=false&limit={total_jobs}&offset=0"

        response = requests.get(api_request)

        if not response.ok:
            print(f"Request to spacecareers.uk was not successful. Code {response.status_code}")
            return []

        results: list[dict[str, Any]] = response.json()["results"]

        jobs_list: list[Job] = []

        for job in results:
            if job["expired"]:
                continue

            advert_url = f"{self._jobsites["space_careers"].url}{job["id"]}"
            description = "" #self._get_space_careers_job_description(advert_url)
            jobs_list.append(self._config_loader.load_space_careers_job(job, advert_url, description))

        return jobs_list

    def _get_space_careers_job_description(self, url: str) -> str:
        with sync_playwright() as sp:
            browser = sp.chromium.launch()
            page = browser.new_page()

            page.goto(url)

            return page.locator("div.wmde-markdown.wmde-markdown-color").inner_text()

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

    def apply_scoring(self, jobs_list: list[Job]):
        for job in jobs_list:
            for country, score in self._config_loader.scoring["country"].items():
                if country in job.country:
                    job.score += score

            for title, score in self._config_loader.scoring["title"].items():
                if title in job.title:
                    job.score += score

            for city, score in self._config_loader.scoring["city"].items():
                if city in job.city:
                    job.score += score

