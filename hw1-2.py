import pickle
import pandas as pd
import requests
import streamlit as st

from user_definition import *


def retrieve_data_from_urls(url_list: list) -> list:
    """
    Read data from url_list and return
    a list of unique dictionaries
    which includes all the data from url in url_list.
    """
    all_jobs = []
    seen = set()

    for url in url_list:
        response = requests.get(url)
        jobs = pickle.loads(response.content)  # each file is a list of dicts
        for job in jobs:
            key = (job["title"], job["link"])
            if key not in seen:
                seen.add(key)
                all_jobs.append(job)

    return all_jobs


def filter_by_company(data: pd.DataFrame, company_dictionary: dict) -> pd.DataFrame:
    """
    For the given data (data frame) and company_dictionary,
    create checkboxes and return a new dataframe
    which only includes data being checked.
    """
    st.sidebar.write("Filter by Company")
    selected = []
    for company, substring in company_dictionary.items():
        if st.sidebar.checkbox(company):
            selected.append(substring)

    if not selected:
        return pd.DataFrame(columns=data.columns)

    mask = data["link"].apply(lambda link: any(sub in link for sub in selected))
    return data[mask]


if __name__ == "__main__":
    st.title(f"{role_name} Job Listings")

    jobs = retrieve_data_from_urls(url_list)
    df = pd.DataFrame(jobs)

    if not df.empty:
        df = df[["date", "title", "link"]]

    filtered_df = filter_by_company(df, company_dictionary)

    st.dataframe(
        filtered_df,
        column_config={
            "link": st.column_config.LinkColumn("Job Link")
        }
    )
