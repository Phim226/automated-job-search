This is an automated job search script. In the job_data folder there are several json files listing job sites and criteria for disqualifying and scoring that the script uses to rank and filter jobs.

At the time of writing this README there is only one website, spacecareers.co.uk, that is searched. The non-expired jobs are pulled from the website using its API, then the jobs are filtered through the disqualification criteria and finally scored by its title and city.

However hopefully soon the script will handle various other websites. It will eventually search the job sites, accessing their apis if available or attempting to scrape the pages if not. Then aggregate all of them together, filter and score, store them in a database, then prepare a report that can be easily read.