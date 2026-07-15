from automated_job_search.config.job import Job

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

    def apply_scoring(self, jobs_list: list[Job]) -> None:
        country_scores = self.scoring["country"]
        city_scores = self.scoring["city"]
        title_scores = self.scoring["title"]

        for job in jobs_list:
            for country, score in country_scores.items():
                if country in job.country:
                    job.score += score

            for city, score in city_scores.items():
                if city in job.city:
                    job.score += score

            for title, score in title_scores.items():
                if title in job.title:
                    job.score += score