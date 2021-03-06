"""
This file implements data types for describing trajectories that we will be plotting
"""

import numpy as np
import matplotlib.pylab as pl
import matplotlib.animation as animation
from MotionAnimation.PY import graphics as grpx

class Trajectory(object):
    """
    class Trajectory
    Base class implementing the interface for a trajectory

        class properties:
        - _time (A list of time points at which the sample values are available)
        - _X (List of associated values for each time point - NUMPY array)

    """

    OBJ_TYPE_LINE = 'line'
    OBJ_TYPE_DOT  = 'point'

    def __init__(self, t_vals=np.array(()), x_vals=None):
        # Data labels and auxiliary information
        self._AXES_IDENTIFIER = None
        self._data_label      = ['x']
        self._X_lims          = None

        # Data values
        self._time = t_vals
        self._X    = self._checkDataSize(x_vals)

    def enforceLimits(self):
        if self._X_lims is None:
            return

        pl.xlim(self._X_lims)

    def setLims(self, x_lims):
        self._X_lims = x_lims

    def getNTrajectories(self):
        """
        The value returned by this function helps us distinguish a single
        trajectory from a set of trajectories
        """
        return(1)

    def getTPts(self, *opts):
        """
        Optional variable number of arguments *opts are not used. They are only
        here to maintain consistency with the calling syntax for a trajectory
        set
        """
        return self._time

    def getAxisLabel(self, ax_idx):
        """
        Get a label string corresponding to the index of data.

        :ax_idx: Index of the data entry. For a 3D trajectory, by default,
            ax_idx 0 would mean 'x', ax_idx 1 would mean 'y', etc.
        :returns: String associated with the data
        """

        return self._data_label[ax_idx]

    def getAxisIdentifier(self):
        return(self._AXES_IDENTIFIER)

    def getContainer(self, object_type=None, figure_handle=None):
        # Get a graphics container that can be used to overlay trajectory with
        # other data (Example: Objects in the environment)
        return getFigureHandle(self._AXES_IDENTIFIER, object_type, in_fhandle=figure_handle)

    def _checkDataSize(self, data):
        """
        _checkDataSize(self, data)
        After the TIME data has been set up, everythin else must match the
        dimensions of the time data. This function checks for the dimesions. If
        a NoneType object is supplied as data, ALL ZEROS are returned with the
        appropriate size, otherwise, a size check is performed.
        """

        # Check the size of t_vals and set x_vals appropriately
        if data is None:
            data = np.zeros(self._time.shape)
        elif (data.shape != self._time.shape):
            raise Exception("Data dimensions not matched. Expect TIME data to match sample values in size")
        return data

    def plotTimedTR(self, object_type=None, figure_handle=None):
        """
        plotTimedTR(self, object_type, figure_handle)
        Function is used to animate the trajectories in time

        :figure_handle: Handle to a window in which the trajectory should be
            plotted
        :object_type: The category of graphics object that needs to be drawn.
            Current choices are line and point.
        :returns: TRUE is plot went through successfully, raises appropriate
            exception otherwise

        """

        figure_handle = getFigureHandle(self._AXES_IDENTIFIER, object_type, in_fhandle=figure_handle)
        figure_handle.animate(self)
        return(True)

    def plotStaticTR(self, object_type=None, figure_handle=None, show=True, show_start_stop=True):
        """
        plotStaticTR(self, object_type, figure_handle)
        Function is used to plot the trajectory data as a static plot in the
        figure window specified by figure_handle

        :figure_handle: Handle to a window in which the trajectory should be
            plotted
        :object_type: The category of graphics object that needs to be drawn.
            Current choices are line and point.
        :show: Determines whether the figure is displayed at the end of the
            function call or not
        :returns: TRUE if the plot went through successfully, raises
            appropriate exception otherwise.

        """

        list_of_sample_values   = self.getSampleValues()
        figure_handle = getFigureHandle(self._AXES_IDENTIFIER, object_type, in_fhandle=figure_handle)
        figure_handle.plot(*list_of_sample_values)

        if show_start_stop:
        # Optional: Can be disabled by passing in appropriate argument
        # Show the first and the last points in the trajectory separately
            start_point = []
            end_point   = []
            for data in list_of_sample_values:
                start_point.append(data[0])
                end_point.append(data[-1])

            # Show the start and end points
            figure_handle.plot(*start_point, 'bo')
            figure_handle.plot(*end_point, 'rs')

        self.enforceLimits()

        if (show):
            figure_handle.show()

        return(figure_handle.getFigureWindow())

    def plot(self, figure_handle=None, axes_handles=None, show=True):
        """
        Show a vanilla plot with Time on the X-axis and one variable of the
        trajectory along the Y-axis. In case of multi-dimensional trajectories,
        different subplots are done for different trajectory variables (x,y,
        and z).

        :figure_handle: Unlike the other functions, here, figure_handle is the
            figure window in which the data must be plotted.
        :axes_handles: In case a figure window is supplied, the axes handles
            can also be supplied in which the individual coordinates have to be
            plotted.
        :returns: the figure_handle and the axes_handles used for plotting.

        """
        timestamps            = self.getTPts()
        list_of_sample_values = self.getSampleValues()
        n_vars_to_plot        = len(list_of_sample_values)

        if figure_handle is None:
            # Start a new figure window
            figure_handle = pl.figure()

        if axes_handles is not None:
            # Make sure that the correct number of axes handles have been
            # supplied - one for each variable to be plotted.
            assert(len(axes_handles) == n_vars_to_plot)
        else:
            # Creating new axes handles
            axes_handles = []
            for tr_idx in range(n_vars_to_plot):
                ax = figure_handle.add_subplot(n_vars_to_plot, 1, 1+tr_idx)
                ax.xaxis.set_label_text('Time')
                ax.yaxis.set_label_text(self.getAxisLabel(tr_idx))
                axes_handles.append(ax)

        # Instead of getting a figure handle which does a state space plot, we
        # just plot the timed trajectory
        for tr_idx, tr_var in enumerate(list_of_sample_values):
            axes_handles[tr_idx].plot(timestamps, list_of_sample_values[tr_idx])

        if show:
            pl.show(figure_handle)

        return figure_handle, axes_handles

    def getSampleValues(self, *opts):
        """
        getSampleValues(self, *opts)
        Gets you a list of values that can directly be piped into PL for
        plotting.

        :*opts: Variable input argument list not used by the function. It is
            here to maintain consistency with the calling syntax for trajectory
            set class
        :returns: The sample values of the trajectory as a list of numpy arrays.

        """

        return [self._X]

    def update(self, *values):
        """
        Updated the values already available in the trajectory.
        Takes in a list of lists (The number of lists put in should match the
        class's expectations), for example, 2 for 1D trajectory (time, X).
        """
        self._time = np.append(self._time, values[0])
        self._X = np.append(self._X, values[1])
        return

class Trajectory__2D(Trajectory):
    """
    class Trajectory__2D 

    """

    def __init__(self, t_vals=np.array(()), x_vals=None, y_vals=None):
        super(Trajectory__2D, self).__init__(t_vals, x_vals)
        self._data_label.append('y')
        self._Y      = self._checkDataSize(y_vals)
        self._Y_lims = [0, 0]

    def setLims(self, x_lims, y_lims):
        self._X_lims = x_lims
        self._Y_lims = y_lims

    def enforceLimits(self):
        super(Trajectory__2D, self).enforceLimits()
        if self._Y_lims is None:
            return

        pl.ylim(self._Y_lims)

    def getSampleValues(self, *opts):
        """
        getSampleValues(self) [PROTECTED FUNCTION]

        :returns: A list of [X, Y] sample values

        """
       
        return [self._X, self._Y]

    def update(self, *values):
        """
        Updated the values already available in the trajectory.
        Takes in a list of lists (The number of lists put in should match the
        class's expectations), for example, 2 for 1D trajectory (time, X).
        """
        super(Trajectory__2D, self).update(values[0], values[1])
        self._Y = np.append(self._Y, values[2])
        return

class Trajectory__3D(Trajectory__2D):
    """
    class Trajectory__3D

    """

    def __init__(self, t_vals, x_vals, y_vals, z_vals):
        super(Trajectory__3D, self).__init__(t_vals, x_vals, y_vals)
        self._data_label.append('z')
        self._AXES_IDENTIFIER = '3d'
        self._Z      = self._checkDataSize(z_vals)
        self._Z_lims = [0, 0]

    def setLims(self, x_lims, y_lims, z_lims):
        self._X_lims = x_lims
        self._Y_lims = y_lims
        self._Z_lims = z_lims

    def enforceLimits(self):
        super(Trajectory__3D, self).enforceLimits()
        if self._Z_lims is None:
            return

        pl.zlim(self._Z_lims)
    
    def getSampleValues(self, *opts):
        """
        getSampleValues(self) [PROTECTED FUNCTION]

        :returns: A list of [X, Y, Z] sample values

        """
       
        return [self._X, self._Y, self._Z]

    def update(self, *values):
        """
        Updated the values already available in the trajectory.
        Takes in a list of lists (The number of lists put in should match the
        class's expectations), for example, 2 for 1D trajectory (time, X).
        """
        super(Trajectory__3D, self).update(values[0], values[1], values[2])
        self._Z = np.append(self._Z, values[3])
        return

class TrajectorySet(object):
    """
    A set of trajectories (all of which may or may not be of the same kind but
    need to be plotted together for visualization)
    """

    def __init__(self):
        """
        class constructor 
        """
        self._AXES_IDENTIFIER = None
        self._tr_set = []
        
    def getNTrajectories(self):
        return(len(self._tr_set))

    def getTPts(self, index=0):
        """
        getTPts(self, index)
        Function returns the time points for the trajectory specified by index

        :index: The index of the trajectory for which the time points are
            required
        """
        if (index > len(self._tr_set)):
            raise Exception("Index access out of the set range")

        return self._tr_set[index].getTPts()

    def getSampleValues(self, index=0):
        """
        getSampleValues(self, index)
        Function returns the sample values for the trajectory specified by index

        :index: The index of the trajectory for which the sample values are
            required
        """
        # TODO: Maybe we can create a common function to check for indices
        if (index > len(self._tr_set)):
            raise Exception("Index access out of the set range")

        return self._tr_set[index].getSampleValues()

    def append(self, tr):
        """
        Append a new trajectory to the list of trajectories stored in the set

        :tr: An instance of the Trajectory class (or any of its subclasses)
            that we wish to append to the already existing list of trajectories

        """

        trajectory_axis_identifier = tr.getAxisIdentifier()
        if trajectory_axis_identifier is not None:
            self._axis_identifier = trajectory_axis_identifier
        self._tr_set    += [tr]

    def plot(self, figure_handle=None):
        """
        Vanilla plotting of variour coordinates for a set of trajectories

        :figure_handle: Figure window in which the trajectories should be drawn

        """
        n_trajectories = self.getNTrajectories()
        if n_trajectories == 0:
            return

        if figure_handle is None:
            figure_handle = pl.figure()

        figure_handle, axes_handles = self._tr_set[0].plot(figure_handle,show=False)
        for tr_idx in range(1,n_trajectories):
            self._tr_set[tr_idx].plot(figure_handle, show=False)

        pl.show(figure_handle)

    def plotStaticTR(self, figure_handle=None):
        """
        plotStaticTR(self, figure_handle)
        Function for plotting multiple trajectories together

        :figure_handle: Handle for the figure window in which the trajectories
            should be plotted
        """

        figure_handle_ = getFigureHandle(self._AXES_IDENTIFIER, in_fhandle=figure_handle)
        print(figure_handle_)

        for tr in self._tr_set:
            tr.plotStaticTR(figure_handle=figure_handle_, show=False)

        figure_handle_.show()

    def plotTimedTR(self, figure_handle=None):
        """
        plotTimedTR(self, figure_handle)
        Function for plotting multiple animated trajectories that are synchronized
        in time

        :figure_handle: Handle for the figure object in which the trajectories
            should be plotted
        """

        figure_handle = getFigureHandle(self._AXES_IDENTIFIER, in_fhandle=figure_handle)
        figure_handle.animate(self)

def getFigureHandle(axes_identifier, obj_type=None, in_fhandle=None):
    """
    Creates a figure handle object if nothing is provided or returns the same
    handle. Helpful when multiple trajectories have to be plotted together.

    :obj_type: Which plot category is needed - Currently support line and point
    :in_f_handle: input figure handle
    :returns: figure_handle if it is supplied, or creates a new one depending on
        obj_type supplied

    """

    if in_fhandle is None:
        if (obj_type is None) or (obj_type == Trajectory.OBJ_TYPE_LINE):
            in_fhandle = grpx.LineContainer(axes_identifier)
        elif (obj_type == Trajectory.OBJ_TYPE_DOT):
            in_fhandle = grpx.PointContainer(axes_identifier)
        else:
            raise ValueError('Invalid object type: %s for creating graphics container!'% obj_type)

    return in_fhandle

def getTRClass(n_dims):
    """
    getTRClass(n_dims)
    In some cases, the user might have to decide which class needs to be used
    at runtime. We can facilitate this by taking in the number of data
    dimensions as an input and returning a handle to the constructor of the
    appropriate trajectory class

    :n_dims: Number of dimensions for the input
    :returns: Handle to the constructor of the appropriate class

    """

    if (n_dims == 1):
        return Trajectory
    elif (n_dims == 2):
        return Trajectory__2D
    elif (n_dims == 3):
        return Trajectory__3D

    raise Exception("Too many dimensions for a visualizable TRAJECTORY.")
