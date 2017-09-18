"""
This file implements data types for describing trajectories that we will be plotting
"""

import numpy as np
import matplotlib.pyplot as pl
from .graphics import GraphicsContainer

class Trajectory(object):

    """
    class Trajectory
    Base class implementing the interface for a trajectory

        class properties:
        - _time (A list of time points at which the sample values are available)
        - _X (List of associated values for each time point - NUMPY array)

    """

    def __init__(self, t_vals=np.array(()), x_vals=None):

        self._AXES_IDENTIFIER = None
        self._time = t_vals
        self._X    = self._checkDataSize(x_vals)

    def getAxisIdentifier(self):
        return(self._AXES_IDENTIFIER)

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

    def plotTimedTR(self, figure_handle):
        """
        plotTimedTR(self, figure_handle)
        Function is used to animate the trajectories in time

        :figure_handle: Handle to a window in which the trajectory should be
            plotted
        :returns: TRUE is plot went through successfully, raises appropriate
            exception otherwise

        """

        raise NotImplementedError

    def plotStaticTR(self, figure_handle=None, show=True):
        """
        plotStaticTR(self, figure_handle)
        Function is used to plot the trajectory data as a static plot in the
        figure window specified by figure_handle

        :figure_handle: Handle to a window in which the trajectory should be
            plotted
        :show: Determines whether the figure is displayed at the end of the
            function call or not
        :returns: TRUE if the plot went through successfully, raises
            appropriate exception otherwise.

        """

        list_of_sample_values   = self.getSampleValues()

        # TODO: Find a way to set up the figure handle
        if figure_handle is None:
            figure_handle = GraphicsContainer()

        figure_handle.plot(*list_of_sample_values)

        return(True)
        
    def getSampleValues(self):
        """
        getSampleValues(self) [PRIVATE FUNCTION]
        Gets you a list of values that can directly be piped into PL for
        plotting.

        :returns: The sample values of the trajector as a list of numpy arrays.

        """

        return [self._X]

class Trajectory__2D(Trajectory):

    """
    class Trajectory__2D 

    """

    def __init__(self, t_vals, x_vals, y_vals):
        super(Trajectory__2D, self).__init__(t_vals, x_vals)
        self._Y    = self._checkDataSize(y_vals)
    
    def getSampleValues(self):
        """
        getSampleValues(self) [PROTECTED FUNCTION]

        :returns: A list of [X, Y] sample values

        """
       
        return [self._X, self._Y]

class Trajectory__3D(Trajectory__2D):

    """
    class Trajectory__3D

    """

    def __init__(self, t_vals, x_vals, y_vals, z_vals):
        super(Trajectory__3D, self).__init__(t_vals, x_vals, y_vals)
        self._AXES_IDENTIFIER = '3d'
        self._Z    = self._checkDataSize(z_vals)
    
    def getSampleValues(self):
        """
        getSampleValues(self) [PROTECTED FUNCTION]

        :returns: A list of [X, Y, Z] sample values

        """
       
        return [self._X, self._Y, self._Z]

class TrajectorySet(object):

    """
    A set of trajectories (all of which may or may not be of the same kind but
    need to be plotted together for visualization)
    """

    def __init__(self):
        """
        class constructor 
        """
        self._axis_identifier = None
        self._tr_set = []
        
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

    def plotStaticTR(self, figure_handle=None):
        """
        plotStaticTR(self, figure_handle)
        Function for plotting multiple trajectories together

        :figure_handle: Handle for the figure window in which the trajectories should be plotted
        """

        if figure_handle is None:
            figure_handle = GraphicsContainer(self._axis_identifier)

        for tr in self._tr_set:
            tr.plotStaticTR(figure_handle, False)

        figure_handle.show()

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
