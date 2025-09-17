# hw2.py
import json
import pandas as pd
import streamlit as st
from google.cloud import storage
from user_definition import (
    service_account_file_path,
    project_id,
    bucket_name,
    file_name_prefix
)


def retrieve_data_from_gcs(service_account_key: str, project_id: str,
                           bucket_name: str, file_name_prefix: str) -> dict:
    """Retrieve job postings from GCS and return merged dict."""
    client = storage.Client.from_service_account_json(service_account_key,
                                                      project=project_id)
    bucket = client.bucket(bucket_name)
    blobs = list(bucket.list_blobs(prefix=file_name_prefix))

    all_results, job_titles, company_dicts = [], set(), {}

    for blob in blobs:
        data = json.loads(blob.download_as_text())
        job_titles.add(data["job_title"])
        company_dicts.update(data["company_dict"])
        all_results.extend(data["results"])

    return {
        "results": all_results,
        "job_titles": sorted(job_titles),
        "company_dict": dict(sorted(company_dicts.items()))
    }


if __name__ == "__main__":
    gcs_data = retrieve_data_from_gcs(
        service_account_file_path,
        project_id,
        bucket_name,
        file_name_prefix
    )

    st.title(", ".join(gcs_data["job_titles"]))

    st.sidebar.write("Filter by Company")
    selected = []
    for company, substring in gcs_data["company_dict"].items():
        if st.sidebar.checkbox(company):
            selected.append(substring)

    df = pd.DataFrame(gcs_data["results"])
    df = df.drop_duplicates(subset=["title", "link", "date"])

    if selected:
        mask = df["link"].apply(lambda link: any(link.startswith(sub) for sub in selected))
        df = df[mask]

    if not df.empty:
        st.dataframe(
            df[["date", "title", "link"]],
            column_config={"link": st.column_config.LinkColumn("Job Link")}
        )
