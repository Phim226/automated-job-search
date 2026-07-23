from automated_job_search.config import JobDetails
from automated_job_search.report.formatting import JobHTML

class JobsReport:

    def __init__(self, jobs: list[JobDetails], title: str) -> None:
        self.jobs = jobs
        self.title = title
        self.intro = ""

    def set_intro(self, intro: str) -> None:
        self.intro = intro


    @property
    def text(self) -> str:
        text = self.intro
        for job in self.jobs:
            text += JobHTML(job).html

        return text


class TopJobsReport(JobsReport):

    def __init__(self, jobs: list[JobDetails]) -> None:
        super().__init__(jobs, "Top Jobs")

class NewJobsReport(JobsReport):

    def __init__(self, jobs: list[JobDetails]) -> None:
        super().__init__(jobs, "New Jobs")

class ExpiringJobsReport(JobsReport):

    def __init__(self, jobs: list[JobDetails]) -> None:
        super().__init__(jobs, "Jobs Expiring Soon")