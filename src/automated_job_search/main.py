import json
import requests
import sys
import sqlite3
import logging
from automated_job_search.config import ConfigLoader, Jobsite
from automated_job_search.scraper import Scraper
from automated_job_search.definitions import JOB_DATA_DIR
from automated_job_search.storage import JobStorageManager
from automated_job_search.filter import JobFilter
from automated_job_search.report import TopJobsReport, Email

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

def configure_log() -> None:
    global logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # File output
    file_handler = logging.FileHandler("job-scraper.log", encoding = "utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Terminal output
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)


class AutomatedJobSearch:

    def search(self) -> None:
        self._load_json_data()
        self._initialise_objects()

        try:
            # TODO: Reinitialisation should be removed eventually. Tables should persist and be checked for new expirations to keep data valid
            self.jsm.reinitialise_tables()

            self._initial_job_processing()
            self._job_details_processing()
            self._report_jobs()

        except requests.RequestException as error:
            logger.exception(f"Job retrieval failed: {error}")
            sys.exit(1)

        except sqlite3.Error as error:
            logger.error(f"Database query failed: {error}")
            sys.exit(1)

        logger.info("Job scraping completed")



    def _initialise_objects(self):
        self.scraper = Scraper(self.job_sites)
        self.config_loader = ConfigLoader(self.job_sites)
        self.jsm = JobStorageManager(self.job_sites)
        self.filter = JobFilter(self.scoring, self.disqualifiers)

    def _load_json_data(self) -> None:
        self.job_sites = load_sites()
        self.scoring = load_scoring()
        self.disqualifiers = load_disqualifiers()

    def _initial_job_processing(self) -> None:
        jobs_dicts = self.scraper.get_jobs()

        logger.info("Jobs scraped")

        jobs = self.config_loader.load_space_careers_job(jobs_dicts)
        filtered_jobs = self.filter.filter_jobs(jobs)
        self.filter.job_summary_scoring(filtered_jobs)

        self.jsm.save_job_summary(filtered_jobs)

        logger.info("Job summaries saved to database")

    def _job_details_processing(self) -> None:
        minimum_score = 10
        top_jobs_db_records = self.jsm.select_top_scoring_job_summaries(minimum_score)
        top_jobs = self.config_loader.load_job_from_db(top_jobs_db_records)
        top_jobs_ids = [record[0] for record in top_jobs_db_records] # Job ids are required in list form for the retrieval of the job details

        # The function that loads the JobDetails objects takes a list of the Jobs and the associated
        # job details dictionary that is retrieved from space careers website
        job_detail_pair = list(zip(top_jobs, self.scraper.retrieve_spacecareers_job_details(top_jobs_ids)))

        logger.info("Job details scraped")

        job_details = self.config_loader.load_space_careers_job_details(job_detail_pair)
        # TODO: Score job details
        self.jsm.save_job_details(job_details)

        logger.info("Job details saved to database")

    def _report_jobs(self) -> None:
        minimum_score = 10
        top_job_details_db = self.jsm.select_top_scoring_job_details(minimum_score)
        job_details = self.config_loader.load_job_details_from_db(top_job_details_db)
        top_jobs_report = TopJobsReport(job_details)
        Email(top_jobs_report.text, top_jobs_report.title).send_email()

        logger.info("Job reports emailed")

if __name__ == "__main__":
    configure_log()

    ajs = AutomatedJobSearch()
    ajs.search()
