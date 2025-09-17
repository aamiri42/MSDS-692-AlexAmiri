import os
import requests
from dotenv import load_dotenv
from user_definition import company_dictionary, bucket_name

load_dotenv()
base_url = os.getenv("API_SERVICE_URL")

# 1. Test /search/jobs
search_body = {
    "job_title": "Data Scientist",
    "company_dict": company_dictionary  # must match the Pydantic model
}

search_response = requests.post("{}/search/jobs".format(base_url), json=search_body)
print("search_response status:", search_response.status_code)

# 2. Test /save_to_gcs
upload_body = {
    "bucket_name": bucket_name,
    "file_name": "job_search/test.json",
    "content": search_response.text
}

upload_response = requests.put("{}/save_to_gcs".format(base_url), json=upload_body)
print("upload_response status:", upload_response.status_code)
