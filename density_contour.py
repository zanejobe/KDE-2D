import numpy as np
import pandas as pd

from scipy import stats
import statsmodels.nonparametric.api as smnp

import matplotlib.pyplot as plt

from six import string_types


def _kde_support(data, bw, gridsize, cut, clip):
    '''Establish support for a kernel density estimate.'''
    support_min = max(data.min() - bw * cut, clip[0])
    support_max = min(data.max() + bw * cut, clip[1])
    return np.linspace(support_min, support_max, gridsize)

def _statsmodels_bivariate_kde(x, y, bw, gridsize, cut, clip):
    """Compute a bivariate kde using statsmodels."""
    if isinstance(bw, string_types):
        bw_func = getattr(smnp.bandwidths, "bw_" + bw)
        x_bw = bw_func(x)
        y_bw = bw_func(y)
        bw = [x_bw, y_bw]
    elif np.isscalar(bw):
        bw = [bw, bw]

    if isinstance(x, pd.Series):
        x = x.values
    if isinstance(y, pd.Series):
        y = y.values

    kde = smnp.KDEMultivariate([x, y], "cc", bw)
    x_support = _kde_support(x, kde.bw[0], gridsize, cut, clip[0])
    y_support = _kde_support(y, kde.bw[1], gridsize, cut, clip[1])
    xx, yy = np.meshgrid(x_support, y_support)
    z = kde.pdf([xx.ravel(), yy.ravel()]).reshape(xx.shape)
    return xx, yy, z

def _scipy_bivariate_kde(x, y, bw, gridsize, cut, clip):
    """Compute a bivariate kde using scipy."""
    data = np.c_[x, y]
    kde = stats.gaussian_kde(data.T, bw_method=bw)
    data_std = data.std(axis=0, ddof=1)
    if isinstance(bw, string_types):
        bw = "scotts" if bw == "scott" else bw
        bw_x = getattr(kde, "%s_factor" % bw)() * data_std[0]
        bw_y = getattr(kde, "%s_factor" % bw)() * data_std[1]
    elif np.isscalar(bw):
        bw_x, bw_y = bw, bw
    else:
        msg = ("Cannot specify a different bandwidth for each dimension "
               "with the scipy backend. You should install statsmodels.")
        raise ValueError(msg)
    x_support = _kde_support(data[:, 0], bw_x, gridsize, cut, clip[0])
    y_support = _kde_support(data[:, 1], bw_y, gridsize, cut, clip[1])
    xx, yy = np.meshgrid(x_support, y_support)
    z = kde([xx.ravel(), yy.ravel()]).reshape(xx.shape)
    return xx, yy, z

def get_last_color(ax):
    '''Return color of last object plotted on ax. Raises ValueError if ax has no objects.'''
    lines = ax.get_lines()
    if len(lines) == 0:
        raise ValueError("Attempting to get color from axis with no lines")
    else:
        return lines[-1].get_color()

def bivar_kde_contour(x, y, frac=0.9, bw="scott", gridsize=100, cut=3, clip=None, use_package='statsmodels',
                     legend=True, color=None, ax=None, axlabel=True, **kwargs):
    '''Compute kde and plot contour at level containing specified fraction of probability mass.
    
    Parameters
    ----------
    x : 1d array-like
        Input data. Maybe be Pandas series.
    y: 1d array-like
        Second input data.
    bw : {'scott' | 'silverman' | scalar | pair of scalars }, optional
        Name of reference method to determine kernel size, scalar factor,
        or scalar for each dimension of the bivariate plot. Note that the
        underlying computational libraries have different interperetations
        for this parameter: ``statsmodels`` uses it directly, but ``scipy``
        treats it as a scaling factor for the standard deviation of the
        data.
    gridsize : int, optional
        Number of discrete points in the evaluation grid.
    cut : scalar, optional
        Draw the estimate to cut * bw from the extreme data points.
    clip : pair of scalars, or pair of pair of scalars, optional
        Lower and upper bounds for datapoints used to fit KDE. Can provide
        a pair of (low, high) bounds for bivariate plots.
    use_package : {'statsmodels', 'scipy'}, default='statsmodels'
        Specify which packed to use for KDE computation. 
    legend : bool, optional
        If True, add a legend or label the axes when possible.
    color : string or tuple, optional
        Specify color with name, hex code, or RGB tuple. Otherwise auto-generated.
    ax : matplotlib axes, optional
        Axes to plot on, otherwise uses current axes.
    axlabel : bool, optional
        Whether to use x.name, y.name attributes to label axes, if they exist.
    kwargs : key, value pairings
        Other keyword arguments are passed to ``plt.contour{f}`` 
    
    Returns
    -------
    ax : matplotlib Axes
        Axes with plot
    '''

    assert (frac>=0.0 and frac<=1.0), "frac must be in between [0,1]"

    if ax is None:
        ax = plt.gca()
    if color is None:
        scout, = ax.plot([], [])
        color = scout.get_color()
        scout.remove()
    if clip is None:
        clip = [(-np.inf, np.inf), (-np.inf, np.inf)]

    if use_package == 'statsmodels':
        xx, yy, z = _statsmodels_bivariate_kde(x, y, bw, gridsize, cut, clip)
    elif use_package == 'scipy':
        xx, yy, z = _scipy_bivariate_kde(x, y, bw, gridsize, cut, clip)
    else:
        raise ValueError('use_package argument must be one of {"statmodels", "scipy"}')

    z /=  z.sum()               # normalize disttribution to 1
    _z = np.sort(z, axis=None)  # flat, sorted copy

    out_frac = 1 - frac
    value = _z[np.abs(np.cumsum(_z)-out_frac).argmin()]

    ax.contour(xx, yy, z, [value], colors=[color], **kwargs)

    if hasattr(x, "name") and axlabel:
        ax.set_xlabel(x.name)
    if hasattr(y, "name") and axlabel:
        ax.set_ylabel(y.name)

    label = kwargs.pop('label', None)
    if label is not None:
        ax.plot([],[], color=color, label=label)

    return ax, z


