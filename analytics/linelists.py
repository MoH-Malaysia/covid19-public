import os
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from typing import Union
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

    def plot_breakthrough_cases_time_series(self, start_date: str, end_date: str, *, moving_average: int = 7):
        """
        Plot the breakthrough cases as a time-series by vaccine type.

        Parameters
        ----------
        start_date: str
            start date in format "YYYY-MM-DD"
        end_date: str
            end date in format "YYYY-MM-DD"
        moving_average: int
            smooth daily cases using moving average (7-day MA default), set to zero for unsmoothed cases.
        """
        df_case_rate = self.get_breakthrough_cases_time_series(
            start_date, end_date, moving_average=moving_average
        )

        df_effectiveness = pd.DataFrame()
        df_effectiveness["Pfizer-BioNTech"] = self._get_vaccine_effectiveness(
            df_case_rate["Pfizer-BioNTech"].values, df_case_rate["Unvaccinated"].values
        )
        df_effectiveness["Oxford-AstraZeneca"] = self._get_vaccine_effectiveness(
            df_case_rate["Oxford-AstraZeneca"].values, df_case_rate["Unvaccinated"].values
        )
        df_effectiveness["Sinovac"] = self._get_vaccine_effectiveness(
            df_case_rate["Sinovac"].values, df_case_rate["Unvaccinated"].values
        )
        df_effectiveness[df_effectiveness.values < 0] = 0
        df_effectiveness.index = df_case_rate.index

        plt.rcParams.update({'font.size': 12})
        fig = plt.figure(figsize=(6.66, 8), facecolor='w', dpi=100)
        ax_1 = plt.subplot(2, 1, 1)
        df_case_rate.plot(ax=ax_1, color=["r", "lightblue", "orange", "k"])
        ax_1.set_ylabel("Cases per 100,000 people", fontsize=13)
        ax_1.set_title("Malaysia breakthrough cases: Unvaccinated vs. fully vaccinated", fontsize=13)
        plt.ylim([0, 100])
        plt.grid(alpha=0.25)

        ax_2 = plt.subplot(2, 1, 2)
        df_effectiveness.plot(ax=ax_2, color=["lightblue", "orange", "k"])
        ax_2.set_ylabel("Effectiveness against infection (%)", fontsize=13)
        ax_2.set_title("Apparent vaccine effectiveness/waning effect", fontsize=13)
        plt.ylim([0, 100])
        plt.grid(alpha=0.25)
        plt.tight_layout()
        return

    def get_breakthrough_cases_time_series(
            self, start_date: str, end_date: str, *, moving_average: int = 7
    ) -> pd.DataFrame:
        """
        Calculate the daily breakthrough case rate between between the specified time interval.

        Parameters
        ----------
        start_date: str
            start date in format "YYYY-MM-DD"
        end_date: str
            end date in format "YYYY-MM-DD"
        moving_average: int
            smooth daily cases using moving average (7-day MA default), set to zero for unsmoothed cases.

        Returns
        -------
        pd.DataFrame
            Daily breakthrough case rate between between the specified time interval (cases per 100,000 people)
        """
        t_start = pd.to_datetime(start_date) - pd.Timedelta(days=moving_average)
        t_end = pd.to_datetime(end_date)
        process_dates = pd.date_range(t_start, t_end)

        # Get required variables
        df_cases = self.cases.copy()
        df_cases.set_index("date", inplace=True, drop=True)
        df_breakthrough_rate = pd.DataFrame()

        for date in process_dates:
            is_today = (df_cases.index == date)
            df_daily_cases_by_vax = df_cases[["brand1", "brand2", "days_dose2"]][is_today].copy()
            n_cases_by_vax = self._get_statistics_by_vaccination(df_daily_cases_by_vax)
            n_pop_by_vax = self._get_population_by_vaccination_status(date, full_vax_lag=14)

            daily_breakthrough_rate = {
                "Unvaccinated": (n_cases_by_vax["Unvaccinated"] / n_pop_by_vax["Unvaccinated"] * 100000),
                "Pfizer-BioNTech": (n_cases_by_vax["Pfizer-BioNTech"] / n_pop_by_vax["Pfizer-BioNTech"] * 100000),
                "Oxford-AstraZeneca": (
                        n_cases_by_vax["Oxford-AstraZeneca"] / n_pop_by_vax["Oxford-AstraZeneca"] * 100000
                ),
                "Sinovac": (n_cases_by_vax["Sinovac"] / n_pop_by_vax["Sinovac"] * 100000)
            }

            df_day = pd.Series(daily_breakthrough_rate)
            df_breakthrough_rate = pd.concat([df_breakthrough_rate, df_day], axis=1)

        df_breakthrough_rate.columns = process_dates.values
        df_breakthrough_rate = df_breakthrough_rate.T

        if moving_average > 0:
            df_breakthrough_rate = df_breakthrough_rate.rolling(window=moving_average).mean()
            df_breakthrough_rate.dropna(inplace=True)

        # Set Oxford-AstraZeneca to np.nan before 1-Aug-2021 due to small sample size
        is_before_date = df_breakthrough_rate.index <= pd.to_datetime("2021-08-01")
        df_breakthrough_rate["Oxford-AstraZeneca"][is_before_date] = np.nan
        return df_breakthrough_rate

    def plot_breakthrough_deaths_time_series(self, start_date: str, end_date: str, *, moving_average: int = 7):
        """
        Plot the breakthrough deaths as a time-series by vaccine type.

        Parameters
        ----------
        start_date: str
            start date in format "YYYY-MM-DD"
        end_date: str
            end date in format "YYYY-MM-DD"
        moving_average: int
            smooth daily cases using moving average (7-day MA default), set to zero for unsmoothed cases.
        """
        df_death_rate = self.get_breakthrough_deaths_time_series(
            start_date, end_date, moving_average=moving_average
        )

        df_effectiveness = pd.DataFrame()
        df_effectiveness["Pfizer-BioNTech"] = self._get_vaccine_effectiveness(
            df_death_rate["Pfizer-BioNTech"].values, df_death_rate["Unvaccinated"].values
        )
        df_effectiveness["Oxford-AstraZeneca"] = self._get_vaccine_effectiveness(
            df_death_rate["Oxford-AstraZeneca"].values, df_death_rate["Unvaccinated"].values
        )
        df_effectiveness["Sinovac"] = self._get_vaccine_effectiveness(
            df_death_rate["Sinovac"].values, df_death_rate["Unvaccinated"].values
        )
        df_effectiveness[df_effectiveness.values < 0] = 0
        df_effectiveness.index = df_death_rate.index

        plt.rcParams.update({'font.size': 12})
        fig = plt.figure(figsize=(6.66, 8), facecolor='w', dpi=100)
        ax_1 = plt.subplot(2, 1, 1)
        df_death_rate.plot(ax=ax_1, color=["r", "lightblue", "orange", "k"])
        ax_1.set_ylabel("Deaths per 100,000 people", fontsize=13)
        ax_1.set_title("Malaysia breakthrough deaths: Unvaccinated vs. fully vaccinated", fontsize=13)
        plt.grid(alpha=0.25)

        ax_2 = plt.subplot(2, 1, 2)
        df_effectiveness.plot(ax=ax_2, color=["lightblue", "orange", "k"])
        ax_2.set_ylabel("Effectiveness against death (%)", fontsize=13)
        ax_2.set_title("Apparent vaccine effectiveness/waning effect", fontsize=13)
        plt.ylim([0, 102])
        plt.grid(alpha=0.25)
        plt.tight_layout()
        return

    def get_breakthrough_deaths_time_series(
            self, start_date: str, end_date: str, *, moving_average: int = 7
    ) -> pd.DataFrame:
        """
        Calculate the daily breakthrough death rate between between the specified time interval.

        Parameters
        ----------
        start_date: str
            start date in format "YYYY-MM-DD"
        end_date: str
            end date in format "YYYY-MM-DD"
        moving_average: int
            smooth daily cases using moving average (7-day MA default), set to zero for unsmoothed cases.

        Returns
        -------
        pd.DataFrame
            Daily breakthrough death rate between between the specified time interval (deaths per 100,000 people)
        """
        t_start = pd.to_datetime(start_date) - pd.Timedelta(days=moving_average)
        t_end = pd.to_datetime(end_date)
        process_dates = pd.date_range(t_start, t_end)

        # Get required variables
        df_deaths = self.deaths.copy()
        df_deaths.set_index("date", inplace=True, drop=True)
        df_breakthrough_rate = pd.DataFrame()

        for date in process_dates:
            is_today = (df_deaths.index == date)
            df_daily_deaths_by_vax = df_deaths[["brand1", "brand2", "days_dose2"]][is_today].copy()
            n_deaths_by_vax = self._get_statistics_by_vaccination(df_daily_deaths_by_vax)
            n_pop_by_vax = self._get_population_by_vaccination_status(date, full_vax_lag=14)

            daily_breakthrough_rate = {
                "Unvaccinated": (n_deaths_by_vax["Unvaccinated"] / n_pop_by_vax["Unvaccinated"] * 100000),
                "Pfizer-BioNTech": (n_deaths_by_vax["Pfizer-BioNTech"] / n_pop_by_vax["Pfizer-BioNTech"] * 100000),
                "Oxford-AstraZeneca": (
                        n_deaths_by_vax["Oxford-AstraZeneca"] / n_pop_by_vax["Oxford-AstraZeneca"] * 100000
                ),
                "Sinovac": (n_deaths_by_vax["Sinovac"] / n_pop_by_vax["Sinovac"] * 100000)
            }

            df_day = pd.Series(daily_breakthrough_rate)
            df_breakthrough_rate = pd.concat([df_breakthrough_rate, df_day], axis=1)

        df_breakthrough_rate.columns = process_dates.values
        df_breakthrough_rate = df_breakthrough_rate.T

        if moving_average > 0:
            df_breakthrough_rate = df_breakthrough_rate.rolling(window=moving_average).mean()
            df_breakthrough_rate.dropna(inplace=True)

        # Set Oxford-AstraZeneca to np.nan before 15-Aug-2021 due to small sample size
        is_before_date = df_breakthrough_rate.index <= pd.to_datetime("2021-08-15")
        df_breakthrough_rate["Oxford-AstraZeneca"][is_before_date] = np.nan

        return df_breakthrough_rate

    @staticmethod
    def _get_statistics_by_vaccination(df_cases_by_vax: pd.DataFrame) -> dict:
        """
        Calculate number of breakthrough cases/deaths by vaccination type

        Parameters
        ----------
        df_cases_by_vax: pd.DataFrame
            self.cases containing columns of "brand1", "brand2" and "days_dose2" between the selected time interval.

        Returns
        -------
        dict
            number of breakthrough cases by vaccination type
        """
        df_cases_by_vax["brand1"].fillna("Unvaccinated", inplace=True)
        case_by_vax = df_cases_by_vax["brand1"].value_counts()
        n_cases_unvaccinated = case_by_vax["Unvaccinated"]

        is_fully_vaccinated = (df_cases_by_vax["days_dose2"].values > 14)
        df_cases_fully_vax = df_cases_by_vax["brand2"][is_fully_vaccinated].copy()
        n_cases_full_vax = df_cases_fully_vax.value_counts()

        if "Pfizer" not in n_cases_full_vax:
            n_cases_full_vax["Pfizer"] = 0
        if "AstraZeneca" not in n_cases_full_vax:
            n_cases_full_vax["AstraZeneca"] = 0
        if "Sinovac" not in n_cases_full_vax:
            n_cases_full_vax["Sinovac"] = 0

        n_cases_by_vax = {
            "Unvaccinated": n_cases_unvaccinated,
            "Pfizer-BioNTech": n_cases_full_vax["Pfizer"],
            "Oxford-AstraZeneca": n_cases_full_vax["AstraZeneca"],
            "Sinovac": n_cases_full_vax["Sinovac"],
        }
        return n_cases_by_vax

    def _get_population_by_vaccination_status(self, date: pd.Timestamp, *, full_vax_lag: int = 14) -> dict:
        """
        Calculate population numbers by vaccination status.

        Parameters
        ----------
        date: pd.Timestamp
            date of interest
        full_vax_lag: int
            days after second dose to be considered fully vaccinated.

        Returns
        -------
        dict
            population numbers by vaccination type
        """
        lagged_date = date - pd.Timedelta(days=full_vax_lag)
        df_vax_rate = self.vaccination.copy()
        df_vax_rate.set_index("date", inplace=True, drop=True)
        is_today = (df_vax_rate.index == date)
        is_lagged = (df_vax_rate.index == lagged_date)

        n_pop_by_vax = {
            "Date": date,
            "Unvaccinated": (self.population["Malaysia"] - df_vax_rate["cumul_partial"][is_today].values[0]),
            "Pfizer-BioNTech": df_vax_rate["cumul_pfizer_2"][is_lagged].values[0],
            "Oxford-AstraZeneca": df_vax_rate["cumul_az_2"][is_lagged].values[0],
            "Sinovac": df_vax_rate["cumul_sino_2"][is_lagged].values[0],
        }
        return n_pop_by_vax

    @staticmethod
    def _get_vaccine_effectiveness(
            vaccinated_rate: Union[float, np.ndarray], unvaccinated_rate: Union[float, np.ndarray]
    ) -> Union[float, np.ndarray]:
        """
        Calculate vaccine effectiveness relative to unvaccinated group.

        Parameters
        ----------
        vaccinated_rate: Union[float, np.ndarray]
            Case/death rate by vaccine type
        unvaccinated_rate: Union[float, np.ndarray]
            Case/death rate for the unvaccinated group

        Returns
        -------
        Union[float, np.ndarray]
            Vaccine effectiveness relative to unvaccinated group
        """
        return 100 - (vaccinated_rate / unvaccinated_rate * 100)

    def plot_breakthrough_deaths_pdf_by_age(self, density: bool = True):
        """
        Plot the probability density function of breakthrough deaths by age and vaccine type.

        Parameters
        ----------
        density: bool
            True to return density, false returns the frequency
        """
        is_fully_vaccinated = (self.deaths["days_dose2"].values > 21)
        df_bt_deaths = self.deaths[is_fully_vaccinated].copy()

        df_pfizer = df_bt_deaths[df_bt_deaths["brand2"] == "Pfizer"].copy()
        df_az = df_bt_deaths[df_bt_deaths["brand2"] == "AstraZeneca"].copy()
        df_sinovac = df_bt_deaths[df_bt_deaths["brand2"] == "Sinovac"].copy()

        plt.rcParams.update({'font.size': 12})
        fig = plt.figure(figsize=(6.66, 4), facecolor='w', dpi=100)
        ax_1 = plt.subplot(1, 1, 1)
        plot_probability_density_function(
            df_pfizer["age"].values, bins_res=3, density=density, color='lightblue', linewidth=1
        )

        # Lower bin resolution for Oxford-AZ due to low sample size
        plot_probability_density_function(
            df_az["age"].values, bins_res=5, density=density, color='orange', linewidth=1
        )
        plot_probability_density_function(
            df_sinovac["age"].values, bins_res=3, density=density, color='k', linewidth=1
        )
        plt.legend(["Pfizer-BioNTech", "Oxford-AZ", "Sinovac"], loc="upper left")
        plt.xlabel("Age")
        if density:
            plt.ylabel("Density")
        else:
            plt.ylabel("Frequency")

        plt.title("Probability density function: Breakthrough deaths by age")
        plt.xlim([30, 95])
        plt.grid(alpha=0.25)
        plt.tight_layout()
        return
