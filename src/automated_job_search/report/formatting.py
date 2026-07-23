from automated_job_search.config import JobDetails

class JobHTML:

    JOB_TITLE_FONT_SIZE = 14
    DETAILS_FONT_SIZE = 12

    def __init__(self, job_details: JobDetails) -> None:
        self._job_details = job_details

    @property
    def html(self) -> str:
        return rf"""<html>
                    <body>
                        <p style = "font-size:{self.JOB_TITLE_FONT_SIZE}px; "> <b>{self._job_details.title.capitalize()}</b> </p>
                        <p style = "font-size:{self.DETAILS_FONT_SIZE}px; "> Company: {self._job_details.company.capitalize()}</p>
                        <p style = "font-size:{self.DETAILS_FONT_SIZE}px; "> Location: {self._job_details.city.capitalize()}, {self._job_details.country.capitalize()}</p>
                        <p style = "font-size:{self.DETAILS_FONT_SIZE}px; "> Deadline: {self._job_details.deadline}</p>
                        <p style = "font-size:{self.DETAILS_FONT_SIZE}px; "> Advert: <a href = '{self._job_details.advert_url}'>{self._job_details.advert_url}</a></p>
                        <p style = "font-size:{self.DETAILS_FONT_SIZE}px; "> Application: <a href = '{self._job_details.application_url}'> {self._job_details.application_url}</a></p>
                    </body>
                   </html>"""

