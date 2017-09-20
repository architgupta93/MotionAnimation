import matplotlib.pyplot as pl
import matplotlib.animation as animation
import numpy as np

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

        # Parameters for animation
        self._anim_data = []
        self._tpts      = []
        self._ANIMATION_INTERVAL = 25   # Frame rate for animation

        # Storage for all the line plots
        self._lines     = []

    def _nextAnimationFrame(self, step=0):
        """
        _nextAnimationFrame(self, n_steps)
        Local function used for animations of trajectories. If no value for
        'step' or the frame index is provided, this returns the first frame
        (default). It can therefore be used for the initial frame too

        :step: The index of the step or frame at which the system is
        :returns: A Line object which should be plotted at the next animation
            frame
        """

        self._lines = []
        initial_plt_args = []
        for anim_data in self._anim_data:
            initial_plt_args = anim_data[:step+1]

        self.plot(*initial_plt_args)
        return self._lines,

    def animate(self, tpts, *plt_args):
        """
        animate(self, *plt_args)
        Function that plots time-value data as animations in 1, 2 or 3
        dimensions.

        :tpts: Time points at which data will be supplied for animation
        :*plt_args: Inputs data that has to be animated. Each argument in the
            list given by plt_args should have the same number of points as
            tpts
        """

        # FuncAnimation is the animation type where a function is repeatedly
        # called to create the next frame. The other options that can be used
        # for animation (Keep in mind for future use) are:
        # 1. TimedAnimation (Superclass of FuncAnimation)
        # 2. ArtistAnimation (Entire animation is recorded in the form of
        #   Artists already and is just replayed)

        n_frames        = len(tpts)
        self._tpts      = tpts
        self._anim_data = []
        for arg in plt_args:
            self._anim_data.append(arg)

        animation.FuncAnimation(self._figure, self._nextAnimationFrame, np.arange(0, n_frames), \
                init_func=self._nextAnimationFrame, interval=self._ANIMATION_INTERVAL, blit=True)

        self.show()


    def _update(self, *plt_args):
        """
        _update(self, *plt_args)
        Local function used to update an exisiting set of line plots. We can
        append the data supplied in *plt_args to the existing line plots

        :*plt_args: A list of plotting arguments. Each entry in the list
            corresponds to a line plots which we SHOULD already have in the
            plot. We append the exisiting line plots with this data
        :returns: Line object which can be used by matplotlib's animation
            module
        """

        # Make sure that we have the correct number of line plots being fed in
        # as we already have in the current plot.
        assert(len(self._lines) == len(plt_args))

        raise NotImplementedError

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
        pl.ion()
        pl.show(self._axes)
