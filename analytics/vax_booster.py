import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from typing import Union
from matplotlib.ticker import FuncFormatter
from visual_ops.plot_statistics import plot_probability_density_function
from analytics.linelists import Linelists

file_path_vax_booster = "vaccination/vax_booster_combos.csv"


class BoosterAnalytics(Linelists):
    deaths_two_doses: pd.DataFrame
    deaths_boosted: pd.DataFrame

    def __init__(self):
        super().__init__()
        self.cases_boosted: pd.DataFrame = self._get_breakthrough_cases_from_boosted_group()
        self.vax_booster: pd.DataFrame = self._load_vaccination_booster_statistics()

        self._get_breakthrough_deaths_from_vaccinated_group()
        print(" ")

    def _get_breakthrough_cases_from_boosted_group(self) -> pd.DataFrame:
        df_cases = self.cases.copy()
        is_boosted = (df_cases["days_dose3"].values > 14)
        df_cases = df_cases[is_boosted].copy()

        # Rename vaccines to be consistent with vaccination statistics
        cols = ["brand1", "brand2", "brand3"]

        for col in cols:
            df_cases[col] = np.where((df_cases[col] == "Pfizer"), "p", df_cases[col])
            df_cases[col] = np.where((df_cases[col] == "AstraZeneca"), "a", df_cases[col])
            df_cases[col] = np.where((df_cases[col] == "Sinovac"), "s", df_cases[col])

        df_cases["combo"] = df_cases["brand1"] + df_cases["brand2"] + df_cases["brand3"]
        return df_cases

    def _get_breakthrough_deaths_from_vaccinated_group(self) -> pd.DataFrame:
        df_deaths = self.deaths.copy()

        # Rename vaccines to be consistent with vaccination statistics
        cols = ["brand1", "brand2", "brand3"]

        for col in cols:
            df_deaths[col] = np.where((df_deaths[col] == "Pfizer"), "p", df_deaths[col])
            df_deaths[col] = np.where((df_deaths[col] == "AstraZeneca"), "a", df_deaths[col])
            df_deaths[col] = np.where((df_deaths[col] == "Sinovac"), "s", df_deaths[col])

        df_deaths["date_dose3"] = pd.to_datetime(df_deaths["date_dose3"])
        df_deaths["days_dose3"] = (df_deaths["date"] - df_deaths["date_dose3"]).dt.days

        df_deaths["days_between_dose_2_and_positive"] = (
                pd.to_datetime(df_deaths["date_positive"]) - pd.to_datetime(df_deaths["date_dose2"])
        ).dt.days
        df_deaths["days_between_dose_3_and_positive"] = (
                pd.to_datetime(df_deaths["date_positive"]) - pd.to_datetime(df_deaths["date_dose3"])
        ).dt.days

        # Breakthrough deaths from double vaccinated
        is_double_jabbed = (df_deaths["days_between_dose_2_and_positive"].values > 14)
        df_deaths_double = df_deaths[is_double_jabbed].copy()
        df_deaths_double["combo"] = df_deaths_double["brand1"] + df_deaths_double["brand2"]
        self.deaths_two_doses = df_deaths_double.copy()

        # Breakthrough deaths from boosted group
        is_boosted = (df_deaths["days_between_dose_3_and_positive"].values > 14)
        df_deaths_triple = df_deaths[is_boosted].copy()
        df_deaths_triple["combo"] = df_deaths_triple["brand1"] + df_deaths_triple["brand2"] + df_deaths_triple["brand3"]
        self.deaths_boosted = df_deaths_triple.copy()

    def _load_vaccination_booster_statistics(self) -> pd.DataFrame:
        df_vax_stats = self._load_vaccination_statistics()
        df_vax_stats.index = pd.to_datetime(df_vax_stats["date"])

        df_booster_states = pd.read_csv(file_path_vax_booster)
        df_booster_states["date"] = pd.to_datetime(df_booster_states["date"])
        df_vax_booster = df_booster_states.groupby("date").sum()
        df_vax_booster = df_vax_booster.cumsum()
        dates = np.array(df_vax_booster.index)
        df_vax_booster["date"] = dates

        # Get two dose data for Pfizer/BioNTech, Oxford-AZ and Sinovac
        df_two_doses = df_vax_stats.reindex(df_vax_booster.index)
        df_vax_booster["pp"] = (
                df_two_doses["cumul_pfizer_2"] - df_vax_booster["ppp"] - df_vax_booster["ppa"] - df_vax_booster["pps"]
        )
        df_vax_booster["aa"] = (
                df_two_doses["cumul_az_2"] - df_vax_booster["aap"] - df_vax_booster["aaa"] - df_vax_booster["aas"]
        )
        df_vax_booster["ss"] = (
                df_two_doses["cumul_sino_2"] - df_vax_booster["ssp"] - df_vax_booster["ssa"] - df_vax_booster["sss"]
        )
        df_vax_booster.index = np.arange(len(df_vax_booster))
        return df_vax_booster

    def plot_booster_combination(self, percentage: bool = True):
        df_vax_latest = self.vax_booster.copy()
        df_vax_latest.set_index("date", inplace=True)
        date = df_vax_latest.index[-1].strftime("%Y-%m-%d")
        df_vax_latest = df_vax_latest.iloc[-1].copy()

        combos_pf = ["ppp", "ppa", "pps"]
        combos_az = ["aap", "aaa", "aas"]
        combos_sino = ["ssp", "ssa", "sss"]
        columns = ["PF/BNT", "AZ", "Sino"]

        vax_combo = np.zeros((3, 3))
        vax_combo[0, :] = df_vax_latest[combos_pf].values
        vax_combo[1, :] = df_vax_latest[combos_az].values
        vax_combo[2, :] = df_vax_latest[combos_sino].values
        tot_booster_doses = np.sum(vax_combo)

        plt.rcParams.update({'font.size': 18})
        fig = plt.figure(figsize=(6.66, 6.66), facecolor='w', dpi=100)
        ax_1 = plt.subplot(1, 1, 1)
        if percentage:
            df_combo = pd.DataFrame(
                (vax_combo.astype(int) / tot_booster_doses), columns=columns, index=columns
            )
            sns.heatmap(
                df_combo, ax=ax_1, annot=True, fmt=".1%", cmap="Greens", linewidth=0.5, linecolor='k', cbar=False
            )
            ax_1.set_title(
                "Malaysia booster doses administered \n as of {0}: {1:.2f} million"
                .format(date, (tot_booster_doses / 1E6)), fontsize=16
            )
            ax_1.set_ylabel("Primary")
            ax_1.set_xlabel("Booster")
        else:
            df_combo = pd.DataFrame(vax_combo.astype(int), columns=columns, index=columns)
            sns.heatmap(df_combo, annot=True, fmt=".0f", cmap="YlGnBu")

        plt.tight_layout()
        return

    def get_breakthrough_cases_summary_statistics(self, t_start: str, t_end: str) -> pd.Series:
        is_in_time = self.vax_booster["date"].between(
            pd.to_datetime(t_start) - pd.Timedelta(days=14),
            pd.to_datetime(t_end) - pd.Timedelta(days=14)
        )
        df_vax_rate = self.vax_booster[is_in_time].copy()
        df_vax_rate.drop(columns=["date"], inplace=True)
        df_vax_rate = df_vax_rate.mean()

        df_cases_boosted = self.cases_boosted.copy()
        is_in_time = df_cases_boosted["date"].between(
            pd.to_datetime(t_start), pd.to_datetime(t_end)
        )
        df_cases_boosted = df_cases_boosted[is_in_time].copy()
        n_cases_boosted = df_cases_boosted["combo"].value_counts()

        combos = ["ppp", "ssp", "sss"]
        df_breakthrough_rate = pd.Series()

        for combo in combos:
            df_breakthrough_rate[combo] = n_cases_boosted[combo] / df_vax_rate[combo] * 100000

        return df_breakthrough_rate

    def get_breakthrough_deaths_summary(self, t_start: str, t_end: str) -> pd.Series:
        is_in_time = self.vax_booster["date"].between(
            pd.to_datetime(t_start) - pd.Timedelta(days=21),
            pd.to_datetime(t_end) - pd.Timedelta(days=21)
        )
        df_vax_rate = self.vax_booster[is_in_time].copy()
        df_vax_rate.drop(columns=["date"], inplace=True)
        df_vax_rate = df_vax_rate.mean()

        # Get breakthrough deaths from double vaccinated group
        df_deaths_two_doses = self.deaths_two_doses.copy()
        is_in_time = df_deaths_two_doses["date"].between(
            pd.to_datetime(t_start), pd.to_datetime(t_end)
        )
        df_deaths_two_doses = df_deaths_two_doses[is_in_time].copy()
        n_deaths_two_doses = df_deaths_two_doses["combo"].value_counts()

        # Get breakthrough deaths from boosted group
        df_deaths_boosted = self.deaths_boosted.copy()
        is_in_time = df_deaths_boosted["date"].between(
            pd.to_datetime(t_start), pd.to_datetime(t_end)
        )
        df_deaths_boosted = df_deaths_boosted[is_in_time].copy()
        n_deaths_boosted = df_deaths_boosted["combo"].value_counts()
        n_deaths = pd.concat([n_deaths_two_doses, n_deaths_boosted])

        combos = ["pp", "aa", "ss", "ppp", "ssp", "sss"]
        df_breakthrough_rate = pd.Series()

        for combo in combos:
            if combo in n_deaths:
                df_breakthrough_rate[combo] = n_deaths[combo] / df_vax_rate[combo] * 100000
            else:
                df_breakthrough_rate[combo] = 0

        return df_breakthrough_rate

    def plot_breakthrough_deaths_summary(self, t_start: str, t_end: str):
        df_death_rate = self.get_breakthrough_deaths_summary(t_start, t_end)
        df_death_rate.sort_values(ascending=False, inplace=True)

        plt.rcParams.update({'font.size': 18})
        fig = plt.figure(figsize=(6.66, 6.66), facecolor='w', dpi=100)
        ax_1 = plt.subplot(1, 1, 1)
        df_death_rate.plot.bar(ax=ax_1, color="r", rot=0)
        ax_1.grid(alpha=0.25)
        ax_1.set_ylabel("Deaths per 100,000 people")
        ax_1.set_title(f"Malaysia breakthrough deaths: \n {t_start} to {t_end}")
        plt.ylim([0, 1.08 * np.max(np.round(df_death_rate))])

        for i, v in enumerate(df_death_rate):
            ax_1.text(i - 0.20, v + 0.08, '{0:.2f}'.format(v), color='k', fontsize=14)

        plt.tight_layout()

