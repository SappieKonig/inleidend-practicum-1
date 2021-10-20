import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.optimize import curve_fit
from uncertainties import ufloat
from data import *


def first_analysis(subplot1, subplot2):
    """
    Data processing and analysis:
    (F,r)-plot
    """

    subplot1.set_xlabel(r"$z (m)$")
    subplot1.set_ylabel(r"$F (N)$")
    z_af = h_12_af - p + d_m_af + d_m_onder + h_1 + h_2
    subplot1.scatter(z_af, F_af, 'bo', label='Repelling force')
    subplot1.legend()

    subplot2.set_xlabel(r"$z (m)$")
    subplot2.set_ylabel(r"$F (N)$")
    z_aan = h_12_aan - p + d_m_aan + d_m_onder + h_1 + h_2
    subplot2.scatter(z_aan, F_aan, 'ro', label='Attracting force')
    subplot2.legend()


def first_analysis_with_errorbars(subplot1, subplot2):
    """
    Data processing and analysis:
    (F,r)-plot with errorbars
    """

    subplot1.set_xlabel(r"$z_{af} (m)$")
    subplot1.set_ylabel(r"$F_{af} (N)$")
    subplot1.errorbar(r_af, F_af, yerr=np.full(F_aan.shape, u_F), xerr=u_r_af, fmt='bo', label='Attracting force')
    subplot1.legend()

    subplot2.set_xlabel(r"$z_{aan} (m)$")
    subplot2.set_ylabel(r"$F_{aan} (N)$")
    subplot2.errorbar(r_aan, F_aan, yerr=np.full(F_aan.shape, u_F), xerr=u_r_aan, fmt='ro', label='Repelling force')
    subplot2.legend()


def analysis_with_z_to_the_power_minus_4(subplot1, subplot2):
    """
    Theory tells us that there is a relationship between F and z, with F ~ z**(-4).
    To test that, we will plot the best fit against both of our datasets.
    """

    def plot_with_errorbars_and_fit(r, F, u_r, subplot, label, fmt='r'):

        def func(z, a):
            return a / z ** 4

        popt, pcov = curve_fit(func, r, F, sigma=np.full(F.shape, u_F), absolute_sigma=True)

        print(popt[0], np.sqrt(np.diag(pcov)))

        min_value_z = np.amin(r)
        max_value_z = np.amax(r)

        x = np.linspace(min_value_z, max_value_z, 1000)
        y = func(x, popt[0])

        subplot.plot(x, y, 'g', linewidth=1, label='Fit to curve')
        subplot.errorbar(r, F, yerr=np.full(F_aan.shape, u_F), xerr=u_r, fmt=fmt, label=label)

        return popt[0]

    plot_with_errorbars_and_fit(r_af, F_af, u_r_af, subplot1, label='Repelling force', fmt='bo')
    subplot1.set_xlabel(r"$z_{af} (m)$")
    subplot1.set_ylabel(r"$F_{af} (N)$")
    subplot1.legend()


    plot_with_errorbars_and_fit(r_aan, F_aan, u_r_aan, subplot2, label='Attracting force', fmt='ro')
    subplot2.set_xlabel(r"$z_{aan} (m)$")
    subplot2.set_ylabel(r"$F_{aan} (N)$")
    subplot2.legend()


"""
As the measurements of the repelling force result in poor results, it is incredibly urgent we stop to ask why.
A good explanation can be the short range of measurement. In other words, any and all deviances will have had a greater
effect, meaning the result is less trustworthy. In light of this, in further analysis, we will only look at the attracting force.
"""


def residue_analysis(subplot):
    """
    To see if we are using the right function to model our data, we will do residue analysis.
    """

    def func(z, a):
        return a / z ** 4

    popt, pcov = curve_fit(func, r_aan, F_aan, sigma=np.full(F_aan.shape, u_F), absolute_sigma=True)

    subplot.scatter(r_aan, F_aan - func(r_aan, *popt), c='r', label='Attracting force')
    subplot.legend()

    subplot.set_xlabel(r"$z_{aan} (m)$")
    subplot.set_ylabel(r"$F_{aan} (N)$")


"""
The residue analysis shows no clear patterns, so we'll move on without intervening further with our data.
"""


def linear_fit(subplot, include_fit: bool = True, include_error_bars: bool = True):
    """
    To more easily see flaws, we can plot F to r on a linear plot. For this we first need to transform r, through u = r**(-4).
    """

    def func(r, a):
        return a * r ** -4

    def transform(r):
        return r**-4

    popt, pcov = curve_fit(func, r_aan, F_aan, sigma=np.full(F_aan.shape, u_F), absolute_sigma=True)

    r_min = np.amin(r_aan)
    r_max = np.amax(r_aan)

    x = transform(np.linspace(r_min, r_max, 1000))

    u_u_aan, u_aan = dpl.std_approximation(transform, [(r_aan, u_r_aan)], approx_type='calculus', evaluate=True)

    subplot.errorbar(u_aan, F_aan, yerr=np.full(F_aan.shape, u_F) if include_error_bars else None,
                 xerr=u_u_aan if include_error_bars else None, fmt='ro', label='Attracting force')

    if include_fit:
        subplot.plot(x, x*popt[0], c='y', label='Fit to attractive force')
    subplot.legend()


"""
While the error bars blow up, the line still nicely flow between the points.
"""


if __name__ == "__main__":
    fig, axs = plt.subplots(ncols=2)
    analysis_with_z_to_the_power_minus_4(*axs)
    plt.show()