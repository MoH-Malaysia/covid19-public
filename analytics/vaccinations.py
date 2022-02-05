import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import FuncFormatter

file_path_vaccination = "vaccination/vax_malaysia.csv"
file_path_vaccination_by_age = "vaccination/vax_demog_age.csv"


class Vaccinations:
    """
    Vaccination analysis, Malaysia.
    """
    def __init__(self):
        # Load datasets
        self.data: pd.DataFrame = self._load_vaccination_statistics()
        self.data_by_age: pd.DataFrame = self._load_vaccination_by_age_group()
        self.last_updated = self.data["date"].max()
        print(" ")

    @staticmethod
    def _load_vaccination_statistics() -> pd.DataFrame:
        df_vaccination = pd.read_csv(file_path_vaccination)
        df_vaccination["date"] = pd.to_datetime(df_vaccination["date"])
        df_vaccination["cumul_pfizer_2"] = df_vaccination["pfizer2"].cumsum()
        df_vaccination["cumul_sino_2"] = df_vaccination["sinovac2"].cumsum()
        df_vaccination["cumul_az_2"] = df_vaccination["astra2"].cumsum()
        df_vaccination["cumul_pfizer_3"] = df_vaccination["pfizer3"].cumsum()
        df_vaccination["cumul_sino_3"] = df_vaccination["sinovac3"].cumsum()
        df_vaccination["cumul_az_3"] = df_vaccination["astra3"].cumsum()
        df_vaccination["cumul_others_3"] = (
            df_vaccination["cumul_booster"] - df_vaccination["cumul_pfizer_3"] -
            df_vaccination["cumul_az_3"] - df_vaccination["cumul_sino_3"]
        )
        return df_vaccination

    @staticmethod
    def _load_vaccination_by_age_group() -> pd.DataFrame:
        df_vax_age = pd.read_csv(file_path_vaccination_by_age)
        df_vax_age["date"] = pd.to_datetime(df_vax_age["date"])
        df_tot_vax_age = df_vax_age.groupby(by=["date"]).sum()
        return df_tot_vax_age

    def plot_daily_vaccines_administered(self, *, percentage: bool = True):
        df_vax = pd.DataFrame()
        df_vax["Pfizer-BioNTech"] = self.data["pfizer1"] + self.data["pfizer2"] + self.data["pfizer3"]
        df_vax["Oxford-AstraZeneca"] = self.data["astra1"] + self.data["astra2"] + self.data["astra3"]
        df_vax["Sinovac"] = self.data["sinovac1"] + self.data["sinovac2"] + self.data["sinovac3"]
        df_vax["Others"] = self.data["daily"] - df_vax["Pfizer-BioNTech"] - \
                           df_vax["Oxford-AstraZeneca"] - df_vax["Sinovac"]
        df_vax.index = self.data["date"].copy()
        df_vax_weekly = df_vax.resample('W').sum()

        plt.rcParams.update({'font.size': 10})
        fig = plt.figure(figsize=(6.66, 3.33), facecolor='w', dpi=125)
        ax_1 = plt.subplot(1, 1, 1)
        custom_colors = ["dodgerblue", "orange", "r", "grey"]

        if percentage:
            df_pct = pd.DataFrame()
            df_pct["Pfizer-BioNTech"] = df_vax_weekly["Pfizer-BioNTech"] / df_vax_weekly.sum(axis=1)
            df_pct["Oxford-AstraZeneca"] = df_vax_weekly["Oxford-AstraZeneca"] / df_vax_weekly.sum(axis=1)
            df_pct["Sinovac"] = df_vax_weekly["Sinovac"] / df_vax_weekly.sum(axis=1)
            df_pct["Others/Pending"] = df_vax_weekly["Others"] / df_vax_weekly.sum(axis=1)
            df_pct.index = df_vax_weekly.index.copy()
            df_pct.iloc[:-1].plot.area(
                ax=ax_1, y=["Pfizer-BioNTech", "Oxford-AstraZeneca", "Sinovac", "Others/Pending"],
                color=custom_colors
            )
            ax_1.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.0%}'.format(y)))
            ax_1.set_ylim([0, 1])

            # Booster campaign
            date_booster = pd.to_datetime("2021-10-12")
            ax_1.axvline(date_booster, color="k", linestyle=":", linewidth=2)
            ax_1.text((date_booster - pd.Timedelta(days=10)), 0.25, 'Boosters offered', rotation=90)
        else:
            df_vax_weekly.iloc[:-1].plot.area(
                ax=ax_1, y=["Pfizer-BioNTech", "Oxford-AstraZeneca", "Sinovac", "Others/Pending"],
                color=custom_colors
            )

        ax_1.set_xlabel(" ", fontsize=1)
        ax_1.set_title("Malaysia: Weekly vaccines administered")
        plt.legend(bbox_to_anchor=(1.01, 0.65))
        plt.tight_layout()
        return

    def plot_booster_campaign_progress(self):
        sino_eligible = self.data["cumul_sino_2"].shift(90)
        pfizer_eligible = self.data["cumul_pfizer_2"].shift(90)
        az_eligible = self.data["cumul_az_2"].shift(90)
        tot_eligible = sino_eligible + pfizer_eligible + az_eligible

        df_plot = pd.DataFrame()
        df_plot["Eligible"] = tot_eligible.values
        df_plot["Pfizer-BioNTech"] = self.data["cumul_pfizer_3"].values
        df_plot["Oxford-AZ"] = self.data["cumul_az_3"].values
        df_plot["Sinovac"] = self.data["cumul_sino_3"].values
        df_plot["Others/Pending"] = self.data["cumul_others_3"].values
        df_plot.index = self.data["date"]

        start_date = pd.to_datetime("2021-10-25")
        is_after_date = (self.data["date"] > start_date).values
        df_plot = df_plot[is_after_date].copy()

        fig = plt.figure(figsize=(5, 4.5), facecolor='w', dpi=125)
        ax_1 = plt.subplot(1, 1, 1)
        df_plot.plot(ax=ax_1, y=["Eligible"], linestyle="--", color="k", legend=True)
        df_plot.plot.area(ax=ax_1, y=["Pfizer-BioNTech", "Sinovac", "Oxford-AZ", "Others/Pending"],
                          color=["dodgerblue", "r", "orange", "lightgrey"], legend=True)
        plt.ylim([0, 1.25*df_plot["Eligible"].max()])
        ax_1.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
        ax_1.set_xlabel(" ", fontsize=1)
        ax_1.set_title("Malaysia: Booster doses administered")
        plt.tight_layout()
        return

    # TODO: Boosters by age group
