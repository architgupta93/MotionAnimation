"""
This file implements data types for describing trajectories that we will be plotting
"""

import numpy as np
import matplotlib.pyplot as pl

class Trajectory(object):

    """
    class Trajectory
    Base class implementing the interface for a trajectory

        class properties:
        - _time (A list of time points at which the sample values are available)
        - _X (List of associated values for each time point - NUMPY array)

    """

    def __init__(self, t_vals=np.array(()), x_vals=None):
        self._time = t_vals
        self._X    = self._checkDataSize(x_vals)

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

    def plotStaticTR(self, figure_handle=None):
        """
        plotStaticTR(self, figure_handle)
        Function is used to plot the trajectory data as a static plot in the
        figure window specified by figure_handle

        :figure_handle: Handle to a window in which the trajectory should be
            plotted
        :returns: TRUE if the plot went through successfully, raises
            appropriate exception otherwise.

        """

        list_of_sample_values   = self.getSampleValues()

        # TODO: Find a way to set up the figure handle
        pl.plot(*list_of_sample_values)
        pl.show()
        
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
        self._Z    = self._checkDataSize(z_vals)
    
    def getSampleValues(self):
        """
        getSampleValues(self) [PROTECTED FUNCTION]

        :returns: A list of [X, Y, Z] sample values

        """
       
        return [self._X, self._Y, self._Z]
