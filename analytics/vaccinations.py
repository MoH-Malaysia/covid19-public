import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

file_path_vaccination = "vaccination/vax_malaysia.csv"


class Vaccinations:
    """
    Vaccination analysis, Malaysia.
    """
    def __init__(self):
        # Load datasets
        self.data: pd.DataFrame = self._load_vaccination_statistics()
        self.last_updated = self.data["date"].max()
        print(" ")

    @staticmethod
    def _load_vaccination_statistics() -> pd.DataFrame:
        df_vaccination = pd.read_csv(file_path_vaccination)
        df_vaccination["date"] = pd.to_datetime(df_vaccination["date"])
        df_vaccination["cumul_pfizer_2"] = df_vaccination["pfizer2"].cumsum()
        df_vaccination["cumul_sino_2"] = df_vaccination["sinovac2"].cumsum()
        df_vaccination["cumul_az_2"] = df_vaccination["astra2"].cumsum()
        return df_vaccination

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
            df_pct["Others"] = df_vax_weekly["Others"] / df_vax_weekly.sum(axis=1)
            df_pct.index = df_vax_weekly.index.copy()
            df_pct.iloc[:-1].plot.area(ax=ax_1, y=["Pfizer-BioNTech", "Oxford-AstraZeneca", "Sinovac", "Others"],
                                       color=custom_colors)
            ax_1.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.0%}'.format(y)))
            ax_1.set_ylim([0, 1])

            # Booster campaign
            date_booster = pd.to_datetime("2021-10-12")
            ax_1.axvline(date_booster, color="k", linestyle=":", linewidth=2)
            ax_1.text((date_booster - pd.Timedelta(days=10)), 0.25, 'Boosters offered', rotation=90)
        else:
            df_vax_weekly.iloc[:-1].plot.area(ax=ax_1, y=["Pfizer-BioNTech", "Oxford-AstraZeneca", "Sinovac", "Others"],
                                              color=custom_colors)

        ax_1.set_xlabel(" ", fontsize=1)
        ax_1.set_title("Malaysia: Weekly vaccines administered")
        plt.legend(bbox_to_anchor=(1.01, 0.65))
        plt.tight_layout()
        return
