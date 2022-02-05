import os
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from typing import Union
from matplotlib.ticker import FuncFormatter
from visual_ops.plot_statistics import plot_probability_density_function

file_path_linelists = "epidemic/linelist"
file_path_vaccination = "vaccination/vax_malaysia.csv"
file_path_population = "static/population.csv"


class VaccineBooster:
    """
    Detailed analysis of the cases and death from boosted group.

    Data source: https://github.com/MoH-Malaysia/covid19-public/tree/main/epidemic/linelist
    """
    def __init__(self):
        # Load datasets
        self.cases: pd.DataFrame = self._load_linelist_cases()
        self.deaths: pd.DataFrame = self._load_linelist_deaths()
        self.vaccination: pd.DataFrame = self._load_vaccination_statistics()
        self.population: dict = self._load_population_statistics()
        self.last_updated = self.cases["date"].max()
        print(" ")

    @staticmethod
    def _load_linelist_cases() -> pd.DataFrame:
        path_original = os.getcwd()
        os.chdir(file_path_linelists)
        file_names = glob.glob("linelist_cases*")
        df_cases_all = pd.DataFrame()

        for file in file_names:
            df_cases = pd.read_csv(
                file,
                dtype={"days_dose1": float, "days_dose2": float, "days_dose3": float,
                       "brand1": str, "brand2": str, "brand3": str, "vaxtype": str}
            )
            df_cases["date"] = pd.to_datetime(df_cases["date"])
            df_cases_all = pd.concat([df_cases_all, df_cases], axis=0)

        os.chdir(path_original)

        """
        # Rename vaccines to be consistent with linelist_deaths
        cols = ["brand1", "brand2", "brand3"]

        for col in cols:
            df_cases_all[col] = np.where((df_cases_all[col] == "p"), "Pfizer", df_cases_all[col])
            df_cases_all[col] = np.where((df_cases_all[col] == "a"), "AstraZeneca", df_cases_all[col])
            df_cases_all[col] = np.where((df_cases_all[col] == "s"), "Sinovac", df_cases_all[col])
        """

        return df_cases_all


    @staticmethod
    def _load_linelist_deaths() -> pd.DataFrame:
        file_path = "{0}/linelist_deaths.csv".format(file_path_linelists)
        df_deaths = pd.read_csv(file_path)
        df_deaths["date"] = pd.to_datetime(df_deaths["date"])
        df_deaths["date_dose1"] = pd.to_datetime(df_deaths["date_dose1"])
        df_deaths["date_dose2"] = pd.to_datetime(df_deaths["date_dose2"])
        df_deaths["days_dose2"] = (df_deaths["date"] - df_deaths["date_dose2"]).dt.days
        return df_deaths

    @staticmethod
    def _load_vaccination_statistics() -> pd.DataFrame:
        df_vaccination = pd.read_csv(file_path_vaccination)
        df_vaccination["date"] = pd.to_datetime(df_vaccination["date"])
        df_vaccination["cumul_pfizer_2"] = df_vaccination["pfizer2"].cumsum()
        df_vaccination["cumul_sino_2"] = df_vaccination["sinovac2"].cumsum()
        df_vaccination["cumul_az_2"] = df_vaccination["astra2"].cumsum()
        df_vaccination["cumul_pfizer_3"] = df_vaccination["pfizer3"].cumsum()
        df_vaccination["cumul_sino_3"] = df_vaccination["sinovac3"].cumsum()
        return df_vaccination

    @staticmethod
    def _load_population_statistics() -> dict:
        df_population = pd.read_csv(file_path_population)
        df_population.set_index('state', inplace=True)
        df_population = df_population['pop'].copy()
        population_stats = df_population.to_dict()
        return population_stats

    def _get_breakthrough_cases_from_boosted_group(self, start_date: str, end_date: str):
        is_not_boosted = (self.cases["brand3"].values.astype(str) == "nan")
        df_boosted = self.cases[~is_not_boosted].copy()

        t_start = pd.to_datetime(start_date)
        t_end = pd.to_datetime(end_date)
        is_date = df_boosted["date"].between(t_start, t_end, inclusive="both")
        df_boosted = df_boosted[is_date].copy()

        df_vax_brand = df_boosted["brand1"] + df_boosted["brand2"] + df_boosted["brand3"]
        df_vax_brand.value_counts()

        # Experiment
        vax_data = self.vaccination.copy()
        vax_data.set_index("date", inplace=True)

        sino_eligible = vax_data["cumul_sino_2"].shift(90)
        pfizer_eligible = vax_data["cumul_pfizer_2"].shift(180)
        az_eligible = vax_data["cumul_az_2"].shift(180)
        tot_eligible = sino_eligible + pfizer_eligible + az_eligible
        pct_eligible_boosted = vax_data["cumul_booster"] / tot_eligible

        df_plot = pd.DataFrame()
        df_plot["total_boosted"] = vax_data["cumul_booster"].values
        df_plot["total_eligible"] = tot_eligible.values

        est_sino_eligible_boosted = pct_eligible_boosted.values * sino_eligible
        est_pfizer_eligible_boosted = pct_eligible_boosted.values * pfizer_eligible
        cumul_pfizer_3 = vax_data["pfizer3"].cumsum()

        est_sino_rem = cumul_pfizer_3 - est_pfizer_eligible_boosted
        est_sino_eligible_boosted_pfizer = est_sino_eligible_boosted - vax_data["sinovac3"].cumsum()

        est_sino_eligible_boosted[-1]
        est_sino_eligible_boosted_pfizer[-1]
        vax_data["sinovac3"].cumsum()[-1]

        return

