import numpy as np
import matplotlib.pyplot as plt
from typing import List


def plot_probability_density_function(sample: np.ndarray, *, bins_res: float = 1, density: bool = False,
                                      alpha: float = 1, color: str = 'b', linewidth: float = 1):
    """
    Plot the probability density function.

    This has advantages relative to matplotlib.hist() because it allows for the comparison of multiple
    probability density functions.

    Parameters
    ----------
    sample: np.ndarray
        sample dataset
    bins_res: float
        resolution for each bin
    density: bool
        calculate density for each bin if true, otherwise the frequency will be returned.
    alpha: float
        transparency of line plot
    color: str
        colour of line plot
    linewidth: float
        line width of plot
    """
    bins, counts_density = get_probability_density_function(sample, bins_res=bins_res, density=density)
    plt.plot(bins, counts_density, color=color, alpha=alpha, linewidth=linewidth)
    return


def get_probability_density_function(sample: np.ndarray, *, bins_res: float = 1, density: bool = False) \
        -> List[np.ndarray]:
    """
    Calculate the probability density function of the provided sample with a specified bin resolution.

    Parameters
    ----------
    sample: np.ndarray
        sample dataset
    bins_res: float
        resolution for each bin
    density: bool
        calculate density for each bin if true, otherwise the frequency will be returned.

    Returns
    -------
    np.ndarray
        probability density function of sample
    """
    max_min_diff = np.max(sample) - np.min(sample)
    n_bins = int(np.ceil(max_min_diff) / bins_res)

    counts_density, bins = np.histogram(sample, bins=n_bins)
    bins_mid_pt = (bins[:-1] + bins[1:]) / 2

    if density:
        counts_density = counts_density / (np.sum(counts_density) * np.diff(bins))

    return [bins_mid_pt, counts_density]
