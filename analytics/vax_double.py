import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from typing import Union
from matplotlib.ticker import FuncFormatter
from visual_ops.plot_statistics import plot_probability_density_function
from analytics.linelists import Linelists


class DoubleVaxAnalytics(Linelists):
    def __init__(self):
        super().__init__()

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
        if (df_cases_by_vax["brand1"] == "Unvaccinated").sum() == 0:
            n_cases_unvaccinated = 0
        else:
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

    def plot_deaths_by_vaccination_status(self, start_date: str, end_date: str, *, percentage: bool = True):
        df_data = self.get_daily_deaths_by_vaccination_status(start_date, end_date)
        df_data["Partial/Others"] = (
                df_data["Total"] - df_data["Unvaccinated"] - df_data["Pfizer-BioNTech"] -
                df_data["Oxford-AstraZeneca"] - df_data["Sinovac"]
        )
        df_data = df_data[["Unvaccinated", "Partial/Others", "Pfizer-BioNTech",
                           "Oxford-AstraZeneca", "Sinovac", "Total"]].copy()
        df_data_weekly = df_data.resample('W').sum()

        df_pct = pd.DataFrame()
        cols = ["Unvaccinated", "Partial/Others", "Pfizer-BioNTech", "Oxford-AstraZeneca", "Sinovac"]

        custom_colors = ["r", "silver", "dodgerblue", "orange", "k"]
        fig = plt.figure(figsize=(6.66, 3.33), facecolor='w', dpi=125)
        ax_1 = plt.subplot(1, 1, 1)

        if percentage:
            for var in cols:
                df_pct[var] = df_data_weekly[var] / df_data_weekly["Total"]

            df_pct.plot.area(ax=ax_1, y=cols, color=custom_colors)
            ax_1.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.0%}'.format(y)))
            ax_1.set_ylim([0, 1])
        else:
            df_data_weekly.iloc[:-1].plot.area(ax=ax_1, y=cols, color=custom_colors)
            ax_1.set_ylabel("Weekly deaths")

        ax_1.set_title("Malaysia: Weekly deaths by vaccination status")
        plt.legend(bbox_to_anchor=(1.01, 0.6))
        plt.tight_layout()
        return

    def get_daily_deaths_by_vaccination_status(self, start_date: str, end_date: str):
        """
        Calculate the total number of daily deaths by vaccination status

        Parameters
        ----------
        start_date: str
            start date in format "YYYY-MM-DD"
        end_date: str
            end date in format "YYYY-MM-DD"

        Returns
        -------
        pd.DataFrame
            Total number of daily deaths by vaccination status
        """
        t_start = pd.to_datetime(start_date)
        t_end = pd.to_datetime(end_date)
        process_dates = pd.date_range(t_start, t_end)

        # Get required variables
        df_deaths = self.deaths.copy()
        df_deaths.set_index("date", inplace=True, drop=True)
        df_daily_deaths = pd.DataFrame()

        for date in process_dates:
            is_today = (df_deaths.index == date)
            df_daily_deaths_by_vax = df_deaths[["brand1", "brand2", "days_dose2"]][is_today].copy()
            n_deaths_by_vax = self._get_statistics_by_vaccination(df_daily_deaths_by_vax)

            daily_deaths = {
                "Unvaccinated": n_deaths_by_vax["Unvaccinated"],
                "Pfizer-BioNTech": n_deaths_by_vax["Pfizer-BioNTech"],
                "Oxford-AstraZeneca": n_deaths_by_vax["Oxford-AstraZeneca"],
                "Sinovac": n_deaths_by_vax["Sinovac"],
                "Total": len(df_daily_deaths_by_vax)
            }

            df_day = pd.Series(daily_deaths)
            df_daily_deaths = pd.concat([df_daily_deaths, df_day], axis=1)

        df_daily_deaths.columns = process_dates.values
        df_daily_deaths = df_daily_deaths.T
        return df_daily_deaths

    def get_death_statistics_by_vax_status(self, *, past_n_days: int = 14):
        t_end = self.last_updated
        t_start = t_end - pd.Timedelta(days=(past_n_days - 1))
        df_data = self.get_daily_deaths_by_vaccination_status(t_start, t_end)
        df_data["Partial/Others"] = (
                df_data["Total"] - df_data["Unvaccinated"] - df_data["Pfizer-BioNTech"] -
                df_data["Oxford-AstraZeneca"] - df_data["Sinovac"]
        )
        df_data = df_data[["Unvaccinated", "Partial/Others", "Pfizer-BioNTech",
                           "Oxford-AstraZeneca", "Sinovac", "Total"]].copy()
        n_pop_by_vax = self._get_population_by_vaccination_status(t_end, full_vax_lag=14)
        df_deaths_sum = df_data.sum()

        print("In between {0} and {1}:".format(t_start.strftime("%Y-%m-%d"), t_end.strftime("%Y-%m-%d")))
        pop_unvax = n_pop_by_vax["Unvaccinated"] / self.population["Malaysia"] * 100
        pct_unvax_death = df_deaths_sum["Unvaccinated"] / df_deaths_sum["Total"] * 100
        print("  - {0:.1f}% of the unvaccinated population accounted for {1:.1f}% of all deaths"
              .format(pop_unvax, pct_unvax_death))

        vax_types = ["Pfizer-BioNTech", "Oxford-AstraZeneca", "Sinovac"]

        for vax in vax_types:
            pop_bnt = n_pop_by_vax[vax] / self.population["Malaysia"] * 100
            pct_bnt_death = df_deaths_sum[vax] / df_deaths_sum["Total"] * 100
            print("  - {0:.1f}% of the population with (2x) {1} caused {2:.1f}% of all deaths"
                  .format(pop_bnt, vax, pct_bnt_death))


