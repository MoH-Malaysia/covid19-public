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


class Linelists:
    """
    Detailed analysis of the cases, deaths and vaccination of Malaysia's COVID-19 pandemic.

    Data source: https://github.com/MoH-Malaysia/covid19-public/tree/main/epidemic/linelist
    """
    def __init__(self):
        # Load datasets
        self.cases: pd.DataFrame = self._load_linelist_cases()
        self.deaths: pd.DataFrame = self._load_linelist_deaths()
        self.vaccination: pd.DataFrame = self._load_vaccination_statistics()
        self.population: dict = self._load_population_statistics()
        self.last_updated = self.cases["date"].max()

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

        # Rename vaccines to be consistent with linelist_deaths
        cols = ["brand1", "brand2", "brand3"]

        for col in cols:
            df_cases_all[col] = np.where((df_cases_all[col] == "p"), "Pfizer", df_cases_all[col])
            df_cases_all[col] = np.where((df_cases_all[col] == "a"), "AstraZeneca", df_cases_all[col])
            df_cases_all[col] = np.where((df_cases_all[col] == "s"), "Sinovac", df_cases_all[col])

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
        return df_vaccination

    @staticmethod
    def _load_population_statistics() -> dict:
        df_population = pd.read_csv(file_path_population)
        df_population.set_index('state', inplace=True)
        df_population = df_population['pop'].copy()
        population_stats = df_population.to_dict()
        return population_stats

    def plot_cases_by_age_group(self, start_date: str, end_date: str, *, bin_size: int = 3):
        """
        Plot heatmap of daily cases by age group between the specified time interval.

        Parameters
        ----------
        start_date: str
            start date in format "YYYY-MM-DD"
        end_date: str
            end date in format "YYYY-MM-DD"
        bin_size: int
            bin size for each age group
        """
        df_cases_by_age = self._get_cases_by_age_group(start_date, end_date, bin_size=bin_size)

        # Reformat y-axis
        plot_date_str = [" " for x in range(len(df_cases_by_age.index))]

        for i in np.arange(0, len(df_cases_by_age.index), 2):
            plot_date_str[i] = str(df_cases_by_age.index.values[i])

        df_cases_by_age.index = np.array(plot_date_str)
        max_val = df_cases_by_age.max().max()

        plt.rcParams.update({'font.size': 8})
        fig = plt.figure(figsize=(6, 6.66), facecolor='w', dpi=100)
        ax_1 = plt.subplot(1, 1, 1)
        sns.heatmap(df_cases_by_age, cmap='hot_r', ax=ax_1, vmin=0, vmax=max_val,
                    cbar_kws={'label': 'Daily cases'})
        ax_1.set(xlabel="Age Category")
        ax_1.set_title("Malaysia Daily Cases: Breakdown by Age")
        ax_1.yaxis.label.set_visible(False)
        ax_1.patch.set_edgecolor('black')
        plt.tight_layout()
        return

    def _get_cases_by_age_group(
            self, start_date: str, end_date: str, *, bin_size: int = 3, moving_average: int = 7
    ) -> pd.DataFrame:
        """
        Breakdown the daily cases by age group between the specific dates

        Parameters
        ----------
        start_date: str
            start date in format "YYYY-MM-DD"
        end_date: str
            end date in format "YYYY-MM-DD"
        bin_size: int
            bin size for each age group
        moving_average: int
            smooth daily cases using moving average (7-day MA default), set to zero for unsmoothed cases.

        Returns
        -------
        pd.DataFrame
            Breakdown of daily ages by age group
        """
        # Get date interval for analysis
        t_start = pd.to_datetime(start_date) - pd.Timedelta(days=moving_average)
        t_end = pd.to_datetime(end_date)
        dates = pd.date_range(start=t_start, end=t_end)

        df_age_group = self._generate_age_groups(bin_size=bin_size)
        df_cases_by_age = pd.DataFrame()

        for day in dates:
            is_in_day = (self.cases["date"] == day)
            df_day = self.cases[is_in_day].copy()

            bins = pd.IntervalIndex.from_arrays(
                left=df_age_group["Lower bound"].values, right=df_age_group["Upper bound"].values, closed="both"
            )
            df_cases_age_day = pd.cut(df_day["age"].values, bins).value_counts()
            df_cases_age_day.index = df_age_group.index
            df_cases_by_age = pd.concat([df_cases_by_age, df_cases_age_day], axis=1)

        df_cases_by_age.columns = dates
        df_cases_by_age = df_cases_by_age.T
        df_cases_by_age.index = dates.strftime("%Y-%m-%d")

        if moving_average > 0:
            df_cases_by_age = df_cases_by_age.rolling(window=7).mean()
            df_cases_by_age.dropna(inplace=True)

        return df_cases_by_age

    @staticmethod
    def _generate_age_groups(*, bin_size: int) -> pd.DataFrame:
        """
        Generate the intervals for each age groups

        Parameters
        ----------
        bin_size: int
            bin size for each age group

        Returns
        -------
        pd.DataFrame()
            interval of each age groups
        """
        age_group_lb = np.arange(0, 85, bin_size)
        age_group_ub = np.roll(age_group_lb, -1) - 1
        age_group_ub[-1] = 120

        df_age_group = pd.DataFrame(np.vstack((age_group_lb, age_group_ub)).T)
        labels = ["{0}-{1}".format(age_group_lb[i], age_group_ub[i]) for i in range(len(age_group_lb))]
        labels[-1] = "{0}+".format(age_group_lb[-1])
        df_age_group.index = labels
        df_age_group.rename(columns={0: "Lower bound", 1: "Upper bound"}, inplace=True)
        return df_age_group
