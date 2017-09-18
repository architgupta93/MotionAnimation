import matplotlib.pyplot as pl
from mpl_toolkits.mplot3d import Axes3D

class GraphicsContainer(object):

    """
    Parent object for storing graphical structures.  The information stored in
    this object is used for rendering both static and dynamic plots
    """

    def __init__(self, axes_projection=None):
        """
        Class constructor
        :axes_projection: In case a 3D plot is required, axes can be set up for
            it by passing the argument '3d' as axes_projection
        """

        # By default, we have 2D axes.
        self._figure    = pl.figure()     
        self._axes      = pl.axes(projection=axes_projection)
        self._is_3d     = (axes_projection == '3d')
        self._x_label   = 'x'
        self._y_label   = 'y'
        self._z_label   = 'z'

        # Storage for all the line plots
        self._lines     = []
    
    def plot(self, *plt_args):
        """
        plot(self, *plt_args)
        :*plt_args: Variable number of arguments to be plotted (Shouldn't be
        more that 3)
        :returns: Nothing is returned at the end of the function, however, the
            _lines member of the class is updated with the line that was
            plotted
        """
        
        self._lines     += self._axes.plot(*plt_args)

    def show(self):
        """
        show(self)
        Draw the axis and show the underlying data
        """
        
        # Bring the correct figure into focus
        pl.figure(self._figure.number)

        # Set up labels
        self._axes.set_xlabel(self._x_label)
        self._axes.set_ylabel(self._y_label)
        if (self._is_3d):
            self._axes.set_zlabel(self._z_label)
        
        # Display the plot
        pl.show(self._axes)
