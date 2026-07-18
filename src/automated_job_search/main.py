import json
import requests
import sys
import sqlite3
from automated_job_search.config import ConfigLoader, Jobsite
from automated_job_search.scraper.scraper import Scraper
from automated_job_search.definitions import JOB_DATA_DIR
from automated_job_search.storage import JobStorageManager
from automated_job_search.filter.filter import JobFilter

# TODO: Implement database query logging

def load_sites() -> dict[str, Jobsite]:
    with open(JOB_DATA_DIR/"job_sites.json", "r") as file:
        jobsites_list =  json.load(file)

    job_sites = dict()
    for site in jobsites_list:
        job_sites[site["name"]] = (Jobsite(**site))

    return job_sites

def load_scoring() -> dict[str, dict[str, int]]:
    with open(JOB_DATA_DIR/"scoring.json") as file:
        scoring: dict[str, dict[str, int]] = json.load(file)

    return scoring

def load_disqualifiers() -> dict[str, list[str]]:
    with open(JOB_DATA_DIR/"disqualifiars.json") as file:
        disqualifiars: dict[str, list[str]] = json.load(file)

    return disqualifiars


class AutomatedJobSearch:

    def search(self) -> None:
        self._load_json_data()
        self._initialise_all_objects()

        try:
            # TODO: Reinitialisation should be removed eventually. Tables should persist and be checked for new expirations to keep data valid
            self.jsm.reinitialise_tables()

            jobs_dicts = self.scraper.get_jobs()

            jobs = self.config_loader.load_space_careers_job(jobs_dicts)
            filtered_jobs = self.filter.filter_jobs(jobs)
            self.filter.apply_scoring(filtered_jobs)

            self.jsm.save_job_summary(filtered_jobs)

            top_jobs_db_records = self.jsm.select_top_scoring_job_summaries(10)
            top_jobs_ids = [record[0] for record in top_jobs_db_records]

            job_detail_pair = list(zip(top_jobs_db_records, self.scraper.retrieve_spacecareers_job_details(top_jobs_ids)))

            job_details = self.config_loader.load_space_careers_job_details(job_detail_pair)
            self.jsm.save_job_details(job_details)

        except requests.RequestException as error:
            print(f"Job retrieval failed: {error}")
            sys.exit(1)

        except sqlite3.Error as error:
            print(f"Database query failed: {error}")
            sys.exit(1)



    def _initialise_all_objects(self):
        self.scraper = Scraper(self.job_sites)
        self.config_loader = ConfigLoader(self.job_sites)
        self.jsm = JobStorageManager(self.job_sites)
        self.filter = JobFilter(self.scoring, self.disqualifiers)

    def _load_json_data(self) -> None:
        self.job_sites = load_sites()
        self.scoring = load_scoring()
        self.disqualifiers = load_disqualifiers()


if __name__ == "__main__":
    ajs = AutomatedJobSearch()
    ajs.search()
