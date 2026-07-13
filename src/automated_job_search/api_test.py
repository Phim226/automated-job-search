import requests

batch_size: int = 1

jobs = []

""" for i in range(10):
    url = f"https://spacecareers.uk/api/jobs/?limit={batch_size}&offset={batch_size*i}"

    response = requests.get(url)

    print(response.status_code)
    print(response.url)
    print(response.json())

    print(f"Results: {response.json()["results"][0]["title"]}")

    jobs += response.json()["results"]

    print("") """

print(jobs)

url = "https://spacecareers.uk/api/jobs/45f10ecc-8e39-4a29-9139-7208b533cd7e/"

response = requests.get(url)

print(response.status_code)
print(response.url)
print(response.json())

""" def request_space_careers_jobs(): """
