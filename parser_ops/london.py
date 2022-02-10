import pandas as pd
import numpy as np
from analytics.covid_base import CovidBase


class London(CovidBase):
    """
    Dataset 1 - Region > London:
       - newCasesByPublishDate
       - newDeaths28DaysByPublishDate

    Dataset 2 - NHS Region > London:
       - newAdmissions
       - covidOccupiedMVBeds
    """
    def __init__(
            self,
            file_path_cases_deaths: str,
            file_path_admissions: str,
            date_start: str = "2020-10-01"
    ):
        df_data = self._load_london_dataset(file_path_cases_deaths, file_path_admissions, date_start)

        super().__init__(
            location="London", date=df_data.index.values, daily_cases=df_data["cases"].values,
            daily_deaths=df_data["deaths"].values, daily_hospitals=df_data["admissions"].values,
        )
        print(" ")

    @staticmethod
    def _load_london_dataset(
            file_path_cases_deaths: str, file_path_admissions: str, date_start: str,
            *, moving_average: int = 7
    ) -> pd.DataFrame:
        df_cases_deaths = pd.read_csv(file_path_cases_deaths)
        df_cases_deaths["date"] = pd.to_datetime(df_cases_deaths["date"], format="%d/%m/%Y")
        df_cases_deaths.set_index("date", inplace=True)

        df_admissions = pd.read_csv(file_path_admissions)
        df_admissions["date"] = pd.to_datetime(df_admissions["date"])
        df_admissions.set_index("date", inplace=True)

        df_raw = pd.concat(
            [df_cases_deaths[["newCasesByPublishDate", "newDeaths28DaysByPublishDate"]],
             df_admissions["newAdmissions"], df_admissions["covidOccupiedMVBeds"]], axis=1
        )

        df_data = pd.DataFrame()

        if moving_average > 0:
            df_data = pd.DataFrame()
            df_data["cases"] = df_raw["newCasesByPublishDate"].rolling(window=moving_average).mean()
            df_data["deaths"] = df_raw["newDeaths28DaysByPublishDate"].rolling(window=moving_average).mean()
            df_data["admissions"] = df_raw["newAdmissions"].rolling(window=moving_average).mean()
            df_data["mechanical_beds"] = df_raw["covidOccupiedMVBeds"].rolling(window=moving_average).mean()
            df_data.dropna(inplace=True)
        else:
            df_data["cases"] = df_raw["newCasesByPublishDate"].copy()
            df_data["deaths"] = df_raw["newDeaths28DaysByPublishDate"].copy()
            df_data["admissions"] = df_raw["newAdmissions"].copy()
            df_data["mechanical_beds"] = df_raw["covidOccupiedMVBeds"].copy()

        # Get data after date of interest
        is_after_date = (df_data.index.values > pd.Timestamp(date_start))
        df_data = df_data[is_after_date].copy()
        return df_data
