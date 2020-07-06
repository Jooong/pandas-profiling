import contextlib
import warnings

import matplotlib
import matplotlib.cbook
import seaborn as sns
from pandas.plotting import register_matplotlib_converters, deregister_matplotlib_converters
from pkg_resources import resource_filename
import time

setting = [0., 0]
restoring = [0., 0]


@contextlib.contextmanager
def manage_matplotlib_context():
    """Return a context manager for temporarily changing matplotlib unit registries and rcParams.
    """
    originalRcParams = matplotlib.rcParams.copy()

    ## Credits for this style go to the ggplot and seaborn packages.
    ##   We copied the style file to remove dependencies on the Seaborn package.
    ##   Check it out, it's an awesome library for plotting
    customRcParams = {
        'patch.facecolor': '#348ABD',  # blue
        'patch.antialiased': True,
        'font.size': 10.0,
        'figure.edgecolor': '0.50',

        # Seaborn common parameters
        'figure.facecolor': 'white',
        'text.color': '.15',
        'axes.labelcolor': '.15',
        # legend.frameon: False
        'legend.numpoints': 1,
        'legend.scatterpoints': 1,
        'xtick.direction': 'out',
        'ytick.direction': 'out',
        'xtick.color': '.15',
        'ytick.color': '.15',
        'axes.axisbelow': True,
        'image.cmap': 'Greys',
        'font.family': ['sans-serif'],
        'font.sans-serif': ['Arial', 'Liberation Sans', 'Bitstream Vera Sans', 'sans-serif'],
        'grid.linestyle': '-',
        'lines.solid_capstyle': 'round',

        # Seaborn darkgrid parameters
        # .15 = dark_gray
        # .8 = light_gray
        'axes.grid': True,
        'axes.facecolor': '#EAEAF2',
        'axes.edgecolor': 'white',
        'axes.linewidth': 0,
        'grid.color': 'white',

        # Seaborn notebook context
        'figure.figsize': [8.0, 5.5],
        'axes.labelsize': 11,
        'axes.titlesize': 12,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 10,

        'grid.linewidth': 1,
        'lines.linewidth': 1.75,
        'patch.linewidth': .3,
        'lines.markersize': 7,
        'lines.markeredgewidth': 0,

        'xtick.major.width': 1,
        'ytick.major.width': 1,
        'xtick.minor.width': .5,
        'ytick.minor.width': .5,

        'xtick.major.pad': 7,
        'ytick.major.pad': 7
    }

    try:
        tic = time.time()
        register_matplotlib_converters()
        matplotlib.rcParams.update(customRcParams)
        sns.set_style(style="white")
        setting_time = time.time() - tic
        setting[0] += setting_time
        setting[1] += 1
        yield
    finally:
        tic = time.time()
        deregister_matplotlib_converters() # revert to original unit registries
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation)
            matplotlib.rcParams.update(originalRcParams) # revert to original rcParams
        restoring_time = time.time() - tic
        restoring[0] += restoring_time
        restoring[1] += 1
        avg_setting_time = setting[0] / setting[1]
        avg_restoring_time = restoring[0] / restoring[1]
        avg_total_overhead = (setting[0] + restoring[0]) / setting[1]
        print(f">>> setting: {setting_time:.5f} (avg: {avg_setting_time:.5f}) (total: {setting[0]:.3f})")
        print(f">>> restoring: {restoring_time:.5f} (avg: {avg_restoring_time:.5f}) (total: {restoring[0]:.3f})")
        print(f">>> total overhaed: {setting_time + restoring_time:.5f} (avg: {avg_total_overhead:.5f}) (total: {setting[0] + restoring[0]:.3f})")
