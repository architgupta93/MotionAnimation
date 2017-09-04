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
        - __time (A list of time points at which the sample values are available)

    """

    def __init__(self, t_vals=np.array(()), x_vals=None):
        self.__time = t_vals
        self.__X    = self.__checkDataSize(x_vals)

    def __checkDataSize(self, data):
        """
        __checkDataSize(self, data)
        After the TIME data has been set up, everythin else must match the
        dimensions of the time data. This function checks for the dimesions. If
        a NoneType object is supplied as data, ALL ZEROS are returned with the
        appropriate size, otherwise, a size check is performed.
        """

        # Check the size of t_vals and set x_vals appropriately
        if (x_vals == None):
            x_vals = np.zeros(t_vals.shape)
        elif (x_vals.shape != t_vals.shape):
            raise Exception("Data dimensions not matched. Expect TIME data to match sample values in size")


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

    def plotStaticTR(self, figure_handle):
        """
        plotStaticTR(self, figure_handle)
        Function is used to plot the trajectory data as a static plot in the
        figure window specified by figure_handle

        :figure_handle: Handle to a window in which the trajectory should be
            plotted
        :returns: TRUE if the plot went through successfully, raises
            appropriate exception otherwise.

        """

        list_of_sample_values   = self.__getSampleValues()

        # TODO: Find a way to set up the figure handle
        np.plot(*list_of_sample_values)
        np.show()
        
    def __getSampleValues(self):
        """
        __getSampleValues(self) [PRIVATE FUNCTION]
        Gets you a list of values that can directly be piped into PL for
        plotting.

        :returns: The sample values of the trajector as a list of numpy arrays.

        """

        return [self.__X]

class Trajectory__2D(Trajectory):

    """
    class Trajectory__2D 

    """

    def __init__(self, t_vals, x_vals, y_vals):
        self.__Y    = np.array(()) 
    
    def __getSampleValues(self):
        """
        __getSampleValues(self) [PROTECTED FUNCTION]

        :returns: A list of [X, Y] sample values

        """
       
        return [self.__X, self.__Y]

class Trajectory__3D(Trajectory__2D):

    """
    class Trajectory__3D

    """

    def __init__(self, t_vals, x_vals, y_vals, z_vals):
        self.__Z    = np.array(())
    
    def __getSampleValues(self):
        """
        __getSampleValues(self) [PROTECTED FUNCTION]

        :returns: A list of [X, Y, Z] sample values

        """
       
        return [self.__X, self.__Y, self.__Z]
