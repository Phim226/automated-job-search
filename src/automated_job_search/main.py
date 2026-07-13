from automated_job_search.config.config_loader import ConfigLoader
from automated_job_search.scraper.scraper import Scraper

if __name__ == "__main__":
    config_loader = ConfigLoader()
    scraper = Scraper(config_loader)
    spacecareers_jobs = scraper.get_jobs()
    scraper.apply_scoring(spacecareers_jobs)

    print(spacecareers_jobs)