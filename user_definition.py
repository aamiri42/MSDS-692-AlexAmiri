# user_definition.py
import os
from dotenv import load_dotenv

load_dotenv()

# GCP config
project_id = os.getenv("PROJECT_ID")
bucket_name = os.getenv("GCP_BUCKET_NAME")
service_account_file_path = os.getenv("GCP_SERVICE_ACCOUNT_KEY")

# Google Custom Search config
API_KEY = os.getenv("API_KEY")                # <── make sure this exists
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")  # <── make sure this exists
API_SERVICE_URL = os.getenv("API_SERVICE_URL")

# Other defaults
file_name_prefix = "job_search/"
role_name = "Data Scientist"

company_dictionary = {
    "Google": "https://careers.google.com",
    "Amazon": "https://amazon.jobs"
}
