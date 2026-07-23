import sqlite3
import logging
from typing import Any
from automated_job_search.config import Job, Jobsite, JobDetails, JobDB, JobDetailsDB
from automated_job_search.definitions import JOB_DATA_DIR

class JobStorageManager:

    JOB_SUMMARY: str = "job_summary"
    JOB_DETAILS: str = "job_details"
    JOB_SITE: str = "job_site"

    def __init__(self, job_sites: dict[str, Jobsite]) -> None:
        self.job_sites = job_sites
        self.db_path = JOB_DATA_DIR/"job_database.db"

    def drop_tables(self) -> None:
        queries =  [
            f"DROP TABLE IF EXISTS {self.JOB_SUMMARY}",
            f"DROP TABLE IF EXISTS {self.JOB_DETAILS}",
            f"DROP TABLE IF EXISTS {self.JOB_SITE}"
        ]
        with sqlite3.connect(self.db_path) as db:
            for query in queries:
                cursor = db.cursor()
                try:
                    cursor.execute(query)
                except sqlite3.Error:
                    logging.exception(f"Execution failed for query: {query}")
                    raise

    def initialise_tables(self) -> None:
        self.create_tables()
        self.populate_job_sites()

    def reinitialise_tables(self) -> None:
        self.drop_tables()
        self.initialise_tables()

    def create_tables(self) -> None:
        job_site_creation_query = f"""
            CREATE TABLE IF NOT EXISTS {self.JOB_SITE} (
                site_id CHAR(50) PRIMARY KEY,
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
                title CHAR(50),
                job_site CHAR(50),
                date_posted CHAR(50),
                duration CHAR(50),
                deadline CHAR(50),
                rolling_deadline BOOL,
                on_site_remote CHAR(50),
                salary_range_lower CHAR(50),
                salary_range_upper CHAR(50),
                expired BOOL,
                advert_url VARCHAR(1000),
                application_url VARCHAR(1000),
                description TEXT(5000),
                FOREIGN KEY (job_id) REFERENCES {self.JOB_SUMMARY}(job_id),
                FOREIGN KEY (job_site) REFERENCES {self.JOB_SITE}(site_id)
            );
        """
        queries = [
            job_site_creation_query,
            job_summary_creation_query,
            job_details_creation_query
        ]
        with sqlite3.connect(self.db_path) as db:
            for query in queries:
                cursor = db.cursor()
                try:
                    cursor.execute(query)
                except sqlite3.Error:
                    logging.exception(f"Execution failed for query: {query}")
                    raise

    def populate_job_sites(self):
        query = f"""
            INSERT OR IGNORE INTO {self.JOB_SITE} (
                site_id,
                url,
                api
            ) VALUES(?, ?, ?);
        """
        with sqlite3.connect(self.db_path) as db:
            cursor = db.cursor()
            try:
                cursor.executemany(query, self.job_sites.values())
            except sqlite3.Error:
                logging.exception(f"Execution failed for query: {query}")
                raise

    def save_job_summary(self, jobs: list[Job]) -> None:
        query = f"""
            INSERT OR IGNORE INTO {self.JOB_SUMMARY} (
                job_id,
                title,
                company,
                city,
                country,
                job_site,
                score
            ) VALUES(?, ?, ?, ?, ?, ?, ?);
        """
        with sqlite3.connect(self.db_path) as db:
            cursor = db.cursor()
            try:
                cursor.executemany(query, jobs)
            except sqlite3.Error:
                logging.exception(f"Execution failed for query: {query}")
                raise

    def select_top_scoring_job_summaries(self, minimum_score: int) -> list[JobDB]:
        query = f"""
            SELECT * FROM {self.JOB_SUMMARY} WHERE score >= {minimum_score} ORDER BY score DESC;
        """
        return self._select_query(query)

    def save_job_details(self, job_details: list[JobDetails]) -> None:
        query = f"""
            INSERT OR IGNORE INTO {self.JOB_DETAILS} (
                job_id,
                title,
                job_site,
                date_posted,
                duration,
                deadline,
                rolling_deadline,
                salary_range_lower,
                salary_range_upper,
                expired,
                on_site_remote,
                application_url,
                advert_url,
                description
            ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        with sqlite3.connect(self.db_path) as db:
            cursor = db.cursor()
            try:
                db_details = [(*job_detail[:2], job_detail[5], *job_detail[7:]) for job_detail in job_details]
                cursor.executemany(query, db_details)
            except sqlite3.Error:
                logging.exception(f"Execution failed for query: {query}")
                raise

    def select_top_scoring_job_details(self, minimum_score: int) -> list[JobDetailsDB]:
        query = f"""
            SELECT
                {self.JOB_SUMMARY}.job_id,
                {self.JOB_SUMMARY}.title,
                {self.JOB_SUMMARY}.company,
                {self.JOB_SUMMARY}.city,
                {self.JOB_SUMMARY}.country,
                {self.JOB_SUMMARY}.job_site,
                {self.JOB_SUMMARY}.score,
                {self.JOB_DETAILS}.date_posted,
                {self.JOB_DETAILS}.duration,
                {self.JOB_DETAILS}.deadline,
                {self.JOB_DETAILS}.rolling_deadline,
                {self.JOB_DETAILS}.on_site_remote,
                {self.JOB_DETAILS}.salary_range_lower,
                {self.JOB_DETAILS}.salary_range_upper,
                {self.JOB_DETAILS}.expired,
                {self.JOB_DETAILS}.advert_url,
                {self.JOB_DETAILS}.application_url,
                {self.JOB_DETAILS}.description
            FROM {self.JOB_SUMMARY}, {self.JOB_DETAILS}
            WHERE score >= {minimum_score} AND {self.JOB_SUMMARY}.job_id = {self.JOB_DETAILS}.job_id
            ORDER BY score DESC;
        """
        return self._select_query(query)

    def _select_query(self, query) -> list[Any]:
        with sqlite3.connect(self.db_path) as db:
                    cursor = db.cursor()
                    try:
                        cursor.execute(query)
                        result = cursor.fetchall()
                    except sqlite3.Error:
                        logging.exception(f"Execution failed for query: {query}")
                        raise

        return result