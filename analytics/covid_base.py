import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.ticker as mtick
from typing import Union


class CovidBase:
    def __init__(
            self, *, location: str,
            date: np.ndarray, daily_cases: np.ndarray, daily_deaths: np.ndarray,
            daily_hospitals: Union[None, np.ndarray] = None,
    ):
        self.location: str = location
        self.data: pd.DataFrame = self._compile_covid_statistics(
            date, daily_cases, daily_deaths, daily_hospitals
        )
        print(" ")

    @staticmethod
    def _compile_covid_statistics(
            date: np.ndarray, daily_cases: np.ndarray, daily_deaths: np.ndarray,
            daily_hospitals: Union[None, np.ndarray] = None,
    ) -> pd.DataFrame:
        df_stats = pd.DataFrame()
        df_stats["date"] = date
        df_stats["cases"] = daily_cases
        df_stats["deaths"] = daily_deaths

        if daily_hospitals is not None:
            df_stats["hospitals"] = daily_hospitals

        return df_stats

    def plot_normalised_cases_hospitals_deaths(
            self, *,
            date_peak_val: tuple = ("2020-11-01", "2021-02-01"),
            shift_hospitals: int = 7,
            shift_deaths: int = 21,
            landscape: bool = False
    ) -> None:
        """
        Plot the daily COVID cases, hospitalisation and deaths that is indexed to the peak from the previous wave.

        Parameters
        ----------
        date_peak_val: tuple
            Date range of peak values from the previous wave.
        shift_hospitals: int
            Shift hospitalisation metric backwards due to lag.
        shift_deaths: int
            Shift death metric backwards due to lag.
        """
        # Get peak values between dates for normalisation
        t_min = pd.to_datetime(date_peak_val[0])
        t_max = pd.to_datetime(date_peak_val[1])
        is_in_time = self.data["date"].between(t_min, t_max, inclusive=True).values
        cases_peak = self.data["cases"][is_in_time].max()
        hospitals_peak = self.data["hospitals"][is_in_time].max()
        deaths_peak = self.data["deaths"][is_in_time].max()

        # Get normalised rate
        df_plot = pd.DataFrame()
        df_plot["cases_norm"] = self.data["cases"] / cases_peak * 100
        df_plot["hospitals_norm"] = self.data["hospitals"] / hospitals_peak * 100
        df_plot["deaths_norm"] = self.data["deaths"] / deaths_peak * 100
        df_plot["hospitals_norm"] = df_plot["hospitals_norm"].shift(periods=-shift_hospitals)
        df_plot["deaths_norm"] = df_plot["deaths_norm"].shift(periods=-shift_deaths)
        df_plot.index = self.data["date"]

        # Plot data
        plt.rcParams.update({'font.size': 15})

        if landscape:
            fig = plt.figure(figsize=(6.66, 4), facecolor='w', dpi=100)
        else:
            fig = plt.figure(figsize=(6.66, 6.66), facecolor='w', dpi=100)

        ax_1 = plt.subplot(1, 1, 1)
        df_plot.plot(ax=ax_1, y=["cases_norm", "hospitals_norm", "deaths_norm"], legend=False,
                     color=["lime", "blue", "r"], linewidth=2)
        ax_1.axhline(100, color='k', linestyle="--", linewidth=1, alpha=0.8)
        ax_1.set_xlabel(" ", fontsize=1)
        ax_1.set_ylabel(" ", fontsize=1)
        plt.xlim([df_plot.index[0], (df_plot.index[-1] + pd.Timedelta(days=110))])
        plt.ylim([0, 1.15 * df_plot["cases_norm"].max()])
        fmt = '%.0f%%'
        yticks = mtick.FormatStrFormatter(fmt)
        ax_1.yaxis.set_major_formatter(yticks)

        # Add labels
        x_pos = (df_plot.index[-1] + pd.Timedelta(days=3))
        x_pos_lagged = (df_plot.index[-1] + pd.Timedelta(days=(-shift_deaths + 6)))

        ax_1.text(
            x_pos, df_plot["cases_norm"][df_plot["cases_norm"].notna()][-1],
            "Cases", fontsize=11, color='lime', weight="bold"
        )
        ax_1.text(
            x_pos, df_plot["hospitals_norm"][df_plot["hospitals_norm"].notna()][-1],
            "Patients", fontsize=11, color='blue', weight="bold"
        )
        ax_1.text(
            x_pos_lagged, 0.8*df_plot["deaths_norm"][df_plot["deaths_norm"].notna()][-1],
            "Deaths", fontsize=11, color='r', weight="bold"
        )

        ax_1.text((x_pos_lagged - pd.Timedelta(days=30)), 101, "Pre-Omicron Peak", color='k', fontsize=12)
        ax_1.grid(axis="y", alpha=0.4)
        plt.tight_layout()
        return
