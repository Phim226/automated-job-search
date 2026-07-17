import json
import requests
import sys
from automated_job_search.config.config_loader import ConfigLoader
from automated_job_search.scraper.scraper import Scraper
from automated_job_search.definitions import JOB_DATA_DIR
from automated_job_search.storage import ConnectionManager, JobStorageManager
from automated_job_search.config.job import Jobsite
from automated_job_search.filter.filter import JobFilter


def load_sites() -> dict[str, Jobsite]:
    with open(JOB_DATA_DIR/"job_sites.json", "r") as file:
        jobsites_list =  json.load(file)

    job_sites = dict()
    for site in jobsites_list:
        job_sites[site["scraper"]] = (Jobsite(**site))

    return job_sites

def load_filters() -> tuple[dict[str, dict[str, int]], dict[str, list[str]]]:
    with open(JOB_DATA_DIR/"scoring.json") as file:
        scoring: dict[str, dict[str, int]] = json.load(file)

    with open(JOB_DATA_DIR/"disqualifiars.json") as file:
        disqualifiars: dict[str, list[str]] = json.load(file)

    return scoring, disqualifiars


class AutomatedJobSearch:

    def search(self) -> None:
        self._load_json_data()
        self._initialise_all_objects()

        # TODO: Reinitialisation should be removed eventually. Tables should persis and be checked for new expirations to keep data valid
        self.jsm.reinitialise_tables()

        try:
            jobs_dicts = self.scraper.get_jobs()

        except requests.RequestException as error:
            print(f"Job retrieval failed: {error}")
            sys.exit(1)

        jobs = self.config_loader.load_space_careers_job(jobs_dicts)
        filtered_jobs = self.filter.filter_jobs(jobs)
        self.filter.apply_scoring(filtered_jobs)

        self.jsm.insert_job_summary(filtered_jobs)

        top_jobs_db_records = self.jsm.select_top_scoring_job_summaries(10)
        top_jobs = self.config_loader.load_job_from_db(top_jobs_db_records)

        job_detail_pair = list(zip(top_jobs, self.scraper.retrieve_spacecareers_job_details(top_jobs)))

        job_details = self.config_loader.load_space_careers_job_details(job_detail_pair)
        self.jsm.insert_job_details(job_details)

    def _initialise_all_objects(self):
        self.scraper = Scraper(self.job_sites)
        self.config_loader = ConfigLoader(self.job_sites)
        self.con_manager = ConnectionManager(JOB_DATA_DIR/"job_database.db")
        self.jsm = JobStorageManager(self.con_manager, self.job_sites)
        self.filter = JobFilter(self.scoring, self.disqualifiers)

    def _load_json_data(self) -> None:
        self.job_sites = load_sites()
        self.scoring, self.disqualifiers = load_filters()


if __name__ == "__main__":
    ajs = AutomatedJobSearch()
    ajs.search()
