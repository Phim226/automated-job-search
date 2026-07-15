from typing import Any
from automated_job_search.storage.connection_manager import ConnectionManager
from automated_job_search.config.job import Job, Jobsite

class JobStorageManager:

    JOB_SUMMARY: str = "job_summary"
    JOB_DETAILS: str = "job_details"
    JOB_SITE: str = "job_site"

    def __init__(self, connection_manager: ConnectionManager, job_sites: dict[str, Jobsite]) -> None:
        self.con_manager = connection_manager
        self.job_sites = job_sites

    def initialise_tables(self) -> list[Any]:
        results = []
        results.append(self.create_tables())
        results.append(self.populate_job_sites())
        return results

    def create_tables(self) -> list[Any]:
        job_site_creation_query = f"""
            CREATE TABLE IF NOT EXISTS {self.JOB_SITE} (
                site_id CHAR(50) PRIMARY KEY,
                name CHAR(50),
                url CHAR(50),
                api VARCHAR(255)
            );
        """

        job_summary_creation_query = f"""
            CREATE TABLE IF NOT EXISTS {self.JOB_SUMMARY} (
                job_id CHAR(50) PRIMARY KEY,
                title CHAR(50),
                company CHAR(50),
                city CHAR(50),
                country CHAR(50),
                job_site CHAR(50),
                score INT,
                FOREIGN KEY (job_site) REFERENCES {self.JOB_SITE}(site_id)
            );
        """

        job_details_creation_query = f"""
            CREATE TABLE IF NOT EXISTS {self.JOB_DETAILS} (
                job_id CHAR(50) PRIMARY KEY,
                job_site CHAR(50),
                date_posted CHAR(50),
                duration CHAR(50),
                deadline CHAR(50),
                rolling_deadline BOOL,
                expired BOOL,
                advert_url VARCHAR(1000),
                application_url VARCHAR(1000),
                description TEXT(5000),
                FOREIGN KEY (job_id) REFERENCES {self.JOB_SUMMARY}(job_id),
                FOREIGN KEY (job_site) REFERENCES {self.JOB_SITE}(site_id)
            );
        """
        return self.con_manager.chain_query([job_site_creation_query, job_summary_creation_query, job_details_creation_query])

    def populate_job_sites(self):
        queries: list[str] = []
        for site in self.job_sites.values():
            query = f"""
                INSERT OR IGNORE INTO {self.JOB_SITE} (
                    site_id,
                    name,
                    url,
                    api
                ) VALUES(
                    '{site.scraper}',
                    '{site.name}',
                    '{site.url}',
                    '{site.api}'
                )
            """
            queries.append(query)

        return self.con_manager.chain_query(queries)

    def reinitialise_tables(self) -> list[Any]:
        drop_result = self.drop_tables()
        return [self.initialise_tables(), drop_result]

    def drop_tables(self) -> list[Any]:
        drop_summary = f"DROP TABLE IF EXISTS {self.JOB_SUMMARY}"
        drop_details = f"DROP TABLE IF EXISTS {self.JOB_DETAILS}"
        return self.con_manager.chain_query([drop_details, drop_summary])

    def insert_job_summary(self, jobs: list[Job]) -> list[Any]:
        queries: list[str] = []
        for job in jobs:
            query = f"""
                INSERT OR IGNORE INTO {self.JOB_SUMMARY} (
                    job_id,
                    title,
                    company,
                    city,
                    country,
                    job_site,
                    score
                ) VALUES(
                    '{job.job_id}',
                    '{job.title}',
                    '{job.company}',
                    '{job.city}',
                    '{job.country}',
                    '{job.job_site}',
                    {job.score}
                )
            """
            queries.append(query)

        return self.con_manager.chain_query(queries)

    def select_top_scoring_job_summaries(self, minimum_score: int) -> list[tuple[str, str, str, str, str, str, int]]:
        query = f"""
            SELECT * FROM {self.JOB_SUMMARY} WHERE score >= {minimum_score} ORDER BY score DESC;
        """
        return self.con_manager.query(query)