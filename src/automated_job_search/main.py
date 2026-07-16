import json
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

    def __init__(self) -> None:
        job_sites = load_sites()
        config_loader = ConfigLoader(job_sites)
        scraper = Scraper(job_sites)

        con_manager = ConnectionManager(JOB_DATA_DIR/"job_database.db")
        jsm = JobStorageManager(con_manager, job_sites)
        jsm.reinitialise_tables()

        filter = JobFilter(*load_filters())

        jobs = config_loader.load_space_careers_job(scraper.get_jobs())
        filtered_jobs = filter.filter_jobs(jobs)
        filter.apply_scoring(filtered_jobs)

        jsm.insert_job_summary(filtered_jobs)

        top_jobs_db_records = jsm.select_top_scoring_job_summaries(10)
        top_jobs = config_loader.load_job_from_db(top_jobs_db_records)

        job_detail_pair = list(zip(top_jobs, scraper.retrieve_spacecareers_job_details(top_jobs)))

        job_details = config_loader.load_space_careers_job_details(job_detail_pair)
        jsm.insert_job_details(job_details)

    def search(self) -> None:
        pass

if __name__ == "__main__":
    ajs = AutomatedJobSearch()
