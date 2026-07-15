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

    spacecareers_jobs = scraper.get_jobs()
    scraper.apply_scoring(spacecareers_jobs)

    jsm.insert_job_summary(spacecareers_jobs)