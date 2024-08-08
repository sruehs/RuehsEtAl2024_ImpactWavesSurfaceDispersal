import pkg_resources
import types
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import LinearSegmentedColormap

# modified after: https://stackoverflow.com/questions/40428931/package-for-listing-version-of-packages-used-in-a-jupyter-notebook


### General functions help to characterize/identify environment

def _get_imports(session_globals):
    for name, val in session_globals.items():
        if isinstance(val, types.ModuleType):
            # Split ensures you get root package,
            # not just imported function
            name = val.__name__.split(".")[0]

        elif isinstance(val, type):
            name = val.__module__.split(".")[0]
        yield name

def print_imported_package_versions(session_globals):
    """
    Call globals() and pass the result to this function.
    """
    imports = list(set(_get_imports(session_globals)))
    # get the version of the root package from only the name of the package
    # via cross-checking the names of installed packages vs. imported packages
    requirements = []
    for m in pkg_resources.working_set:
        if m.project_name in imports and m.project_name != "pip":
            requirements.append((m.project_name, m.version))
    for r in requirements:
        print("{}=={}".format(*r))



### Classes containing Lagrangian simulation settings



### Plotting functions and classes
    
class ColorSettings:
    blue = (68/255, 119/255, 170/255)
    cyan = (102/255, 204/255, 238/255)
    green = (34/255, 136/255, 51/255)
    yellow = (204/255, 187/255, 68/255)
    red = (238/255, 102/255, 119/255)
    purple = (170/255, 51/255, 119/255)
    grey = (187/255, 187/255, 187/255)

def plot_bathy(grid, colors=[(0.5, 0.5, 0.5), (0.5, 0.5, 0.5)]):
    var = grid.umaskutil
    var.rename({'x': 'lon', 'y': 'lat'})
    cmap_name = 'landgrey'
    cmapland = LinearSegmentedColormap.from_list(cmap_name, colors)
    plt.pcolor(grid.glamu.isel(time_counter=0),
               grid.gphiu.isel(time_counter=0),
               var.where(var != 1).isel(time_counter=0),
               cmap=cmapland,
               shading='nearest')
    
def plot_releasebox(release_name, ax, fs=12):
    if release_name == 'GulfOfLion':
        lonmin = 3
        lonmax = 5.6
        latmin = 42.1
        latmax = 43.5
        step = 0.05  # (appr. every grid cell)

    if release_name == 'SubReg14':
        lonmin = 30.3
        lonmax = 32.3
        latmin = 35
        latmax = 37
        step = 0.05  # (appr. every grid cell)

    if release_name == 'SubReg9':
        lonmin = 15.0
        lonmax = 17.0
        latmin = 36.1
        latmax = 38.1
        step = 0.05  # (appr. every grid cell)

    rect = patches.Rectangle((lonmin, latmin), lonmax-lonmin+step, latmax-latmin+step,
                             linewidth=0.5, edgecolor='k', facecolor='none')
    ax.add_patch(rect)


