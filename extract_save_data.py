# extract_save_data.py
import datetime
import requests
from fastapi import FastAPI
from pydantic import BaseModel
from google.cloud import storage
from user_definition import API_KEY, SEARCH_ENGINE_ID

app = FastAPI()


# --------- Pydantic Models ---------
class GoogleSearch(BaseModel):
    job_title: str
    company_dict: dict


class GcsStringUpload(BaseModel):
    bucket_name: str
    file_name: str
    content: str


# --------- Endpoints ---------
@app.post("/search/jobs")
def search_jobs(search_param: GoogleSearch):
    """Call Google Custom Search API and return results as dict."""
    query_parts = [search_param.job_title] + list(search_param.company_dict.values())
    query = " ".join(query_parts)

    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": API_KEY,
        "cx": SEARCH_ENGINE_ID,
        "q": query,
        "dateRestrict": "d7"  # last 7 days
    }

    resp = requests.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()

    results = []
    items = data.get("items", [])[:100]
    today = datetime.date.today()

    for item in items:
        snippet = item.get("snippet", "")
        date = today
        if "days ago" in snippet:
            try:
                days = int(snippet.split("days ago")[0].split()[-1])
                date = today - datetime.timedelta(days=days)
            except Exception:
                pass
        results.append({
            "title": item.get("title", ""),
            "link": item.get("link", ""),
            "snippet": snippet,
            "date": str(date)
        })

    return {
        "company_dict": search_param.company_dict,
        "job_title": search_param.job_title,
        "results": results
    }


@app.put("/save_to_gcs")
def save_to_gcs(gcs_upload_param: GcsStringUpload):
    """Upload a JSON string to GCS bucket."""
    client = storage.Client()
    bucket = client.bucket(gcs_upload_param.bucket_name)
    blob = bucket.blob(gcs_upload_param.file_name)
    blob.upload_from_string(
        gcs_upload_param.content,
        content_type="application/json"
    )

    return {
        "message": (
            f"file {gcs_upload_param.file_name} has been uploaded to "
            f"{gcs_upload_param.bucket_name} successfully."
        )
    }
