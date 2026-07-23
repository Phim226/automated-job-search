from typing import Any
from automated_job_search.config import Job, JobDetails
from automated_job_search.definitions import Disqualifiers, Scores

class JobFilter:

    def __init__(self, scoring: Scores, disqualifiers: Disqualifiers) -> None:
        self.scoring = scoring
        self.disqualifiers = disqualifiers


    def first_job_filter(self, jobs_list: list[Job]) -> list[Job]:
        filtered_list = []
        job_disqualified = False
        for job in jobs_list:
            assert isinstance(self.disqualifiers["title"], list)
            for title_disqualifer in self.disqualifiers["title"]:
                if title_disqualifer in job.title:
                    job_disqualified = True
                    break

            if job_disqualified:
                job_disqualified = False
                continue

            filtered_list.append(job)

        return filtered_list

    def filter_details(self, details_list: list[JobDetails]) -> list[JobDetails]:
        filtered_list = []
        job_disqualified = False
        for job in details_list:
            try:
                salary_range_lower = job.salary_range_lower
                salary_lower = float(salary_range_lower) if salary_range_lower else 0

            except ValueError:
                salary_lower = 0

            assert isinstance(self.disqualifiers["max_salary"], float)
            if salary_lower > self.disqualifiers["max_salary"]:
                job_disqualified = True

            if job_disqualified:
                job_disqualified = False
                continue

            filtered_list.append(job)

        return filtered_list


    def job_summary_scoring(self, jobs_list: list[Job]) -> None:
        scored_fields = ["country", "city", "title"]
        for job in jobs_list:
            for field in scored_fields:
                job.score += self._apply_scoring(field, job)


    def _apply_scoring(self, field: str, job: Job | JobDetails) -> Any:
        scores = self.scoring[field]
        field_score = 0
        for key, score in scores.items():
            if key in getattr(job, field):
                field_score += score

        return field_score