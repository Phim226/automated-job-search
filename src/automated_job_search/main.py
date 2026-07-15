from automated_job_search.config.config_loader import ConfigLoader
from automated_job_search.scraper.scraper import Scraper
from automated_job_search.definitions import JOB_DATA_DIR
from automated_job_search.storage import ConnectionManager, JobStorageManager

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