from typing import Any
from automated_job_search.storage.connection_manager import ConnectionManager
from automated_job_search.config.job import Job

class JobStorageManager:

    JOB_SUMMARY: str = "job_summary"
    JOB_DETAILS: str = "job_details"
    JOB_SITE: str = "job_site"

    def __init__(self, connection_manager: ConnectionManager) -> None:
        self.cm = connection_manager

    def initialise_tables(self) -> list[Any]:
        job_summary_creation_query = f"""
            CREATE TABLE IF NOT EXISTS {self.JOB_SUMMARY} (
                job_id CHAR(50) PRIMARY KEY,
                title CHAR(50),
                company CHAR(50),
                city CHAR(50),
                country CHAR(50),
                score INT
            );
        """

        job_details_creation_query = f"""
            CREATE TABLE IF NOT EXISTS {self.JOB_DETAILS} (
                job_id CHAR(50),
                date_posted CHAR(50),
                duration CHAR(50),
                deadline CHAR(50),
                rolling_deadline BOOL,
                expired BOOL,
                advert_url VARCHAR(1000),
                application_url VARCHAR(1000),
                description TEXT(5000),
                CONSTRAINT fk_job_summary
                FOREIGN KEY (job_id)
                REFERENCES {self.JOB_SUMMARY}(job_id)
            );
        """
        return self.cm.chain_query([job_summary_creation_query, job_details_creation_query])

    def reinitialise_tables(self) -> list[Any]:
        self.drop_tables()
        return self.initialise_tables()

    def drop_tables(self) -> list[Any]:
        drop_summary = f"DROP TABLE IF EXISTS {self.JOB_SUMMARY}"
        drop_details = f"DROP TABLE IF EXISTS {self.JOB_DETAILS}"
        return self.cm.chain_query([drop_details, drop_summary])

    def insert_job_summary(self, jobs: list[Job]) -> list[Any]:
        queries: list[str] = []
        for job in jobs:
            query = f"""INSERT OR IGNORE INTO {self.JOB_SUMMARY} (
                            job_id,
                            title,
                            company,
                            city,
                            country,
                            score
                        ) VALUES(
                            '{job.job_id}',
                            '{job.title}',
                            '{job.company}',
                            '{job.city}',
                            '{job.country}',
                            {job.score}
                    )"""
            queries.append(query)

        return self.cm.chain_query(queries)