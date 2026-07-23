from typing import Any
from automated_job_search.config import Job, JobDetails

class JobFilter:

    def __init__(self, scoring: dict[str, dict[str, int]], disqualifiers: dict[str, list[str]]) -> None:
        self.scoring = scoring
        self.disqualifiers = disqualifiers


    def filter_jobs(self, jobs_list: list[Job]) -> list[Job]:
        filtered_list = []
        job_disqualified = False
        for job in jobs_list:
            for title_disqualifer in self.disqualifiers["title"]:
                if title_disqualifer in job.title:
                    job_disqualified = True
                    break

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