import pandas as pd
from analytics.covid_base import CovidBase

file_path_cases = "epidemic/cases_malaysia.csv"
file_path_hospitals = "epidemic/hospital.csv"
file_path_deaths = "epidemic/deaths_malaysia.csv"


class Malaysia(CovidBase):
    def __init__(self, date_start: str = "2020-10-01", *, moving_average: int = 7):
        self.date_start = pd.to_datetime(date_start)
        self.moving_average = moving_average
        df_data = self._load_malaysia_datasets()

        super().__init__(
            location="Malaysia", date=df_data.index.values, daily_cases=df_data["cases"].values,
            daily_deaths=df_data["deaths"].values, daily_hospitals=df_data["admissions"].values,
        )
        print(" ")

    def _load_malaysia_datasets(self) -> pd.DataFrame:
        df_cases = self._load_cases_dataset()
        df_hospitals = self._load_hospital_dataset(country_level=True)
        df_deaths = self._load_deaths_dataset()

        df_malaysia = pd.concat(
            [df_cases["cases_new"], df_hospitals[["hosp_covid", "admitted_covid"]],
             df_deaths["deaths_new_dod"]], axis=1
        )

        df_data = pd.DataFrame()

        if self.moving_average > 0:
            df_data = pd.DataFrame()
            df_data["cases"] = df_malaysia["cases_new"].rolling(window=self.moving_average).mean()
            df_data["deaths"] = df_malaysia["deaths_new_dod"].rolling(window=self.moving_average).mean()
            df_data["admissions"] = df_malaysia["hosp_covid"].rolling(window=self.moving_average).mean()
            df_data.dropna(inplace=True)
        else:
            df_data["cases"] = df_malaysia["cases_new"].copy()
            df_data["deaths"] = df_malaysia["deaths_new_dod"].copy()
            df_data["admissions"] = df_malaysia["admitted_covid"].copy()

        # Get data after date of interest
        is_after_date = (df_data.index.values > self.date_start)
        df_data = df_data[is_after_date].copy()
        return df_data

    @staticmethod
    def _load_cases_dataset() -> pd.DataFrame:
        df_cases = pd.read_csv(file_path_cases)
        df_cases["date"] = pd.to_datetime(df_cases["date"])
        df_cases.set_index("date", inplace=True)
        return df_cases

    @staticmethod
    def _load_hospital_dataset(*, country_level: bool = True) -> pd.DataFrame:
        df_hospitals = pd.read_csv(file_path_hospitals)
        df_hospitals["date"] = pd.to_datetime(df_hospitals["date"])
        df_hospitals.set_index("date", inplace=True)

        if country_level:
            return df_hospitals.groupby(pd.Grouper(freq="1D")).sum()
        else:
            return df_hospitals

    @staticmethod
    def _load_deaths_dataset() -> pd.DataFrame:
        df_deaths = pd.read_csv(file_path_deaths)
        df_deaths["date"] = pd.to_datetime(df_deaths["date"])
        df_deaths.set_index("date", inplace=True)
        return df_deaths
