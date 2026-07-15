import requests
import json
from typing import Any
from automated_job_search.config.config_loader import ConfigLoader
from automated_job_search.scraper.scraper import Scraper
from automated_job_search.definitions import JOB_DATA_DIR
from automated_job_search.storage import ConnectionManager, JobStorageManager
from automated_job_search.config.job import Jobsite


class AutomatedJobSearch:

    def __init__(self) -> None:
        jobsites = self._load_sites()
        disqualifiars, scoring = self._load_filters()

    @staticmethod
    def _load_sites() -> dict[str, Jobsite]:
        with open(JOB_DATA_DIR/"job_sites.json", "r") as file:
            jobsites_list =  json.load(file)

        jobsites = dict()
        for site in jobsites_list:
            jobsites[site["scraper"]] = (Jobsite(**site))

        return jobsites

    @staticmethod
    def _load_filters() -> tuple[dict[str, list[str]], dict[str, dict[str, int]]]:
        with open(JOB_DATA_DIR/"disqualifiars.json") as file:
            disqualifiars: dict[str, list[str]] = json.load(file)

        with open(JOB_DATA_DIR/"scoring.json") as file:
            scoring: dict[str, dict[str, int]] = json.load(file)

        return disqualifiars, scoring


if __name__ == "__main__":
    config_loader = ConfigLoader()
    scraper = Scraper(config_loader)

    cm = ConnectionManager(JOB_DATA_DIR/"job_database.db")
    jsm = JobStorageManager(cm, config_loader)
    jsm.reinitialise_tables()

    jobs = config_loader.load_space_careers_job(scraper.get_jobs())
    #scraper.apply_scoring(spacecareers_jobs)

    jsm.insert_job_summary(jobs)

    top_jobs_db_records = jsm.select_top_scoring_job_summaries(10)

    print(config_loader.load_job_from_db(top_jobs_db_records))

    """ url = "https://spacecareers.uk/api/jobs/cc0c6606-7a02-46b8-859a-1cd24332a4be/"

    response = requests.get(url)
    print(response.json()) """