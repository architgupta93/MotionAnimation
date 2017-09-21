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

        # Include a pointer to the trajectory object
        self._tr_obj    = []

        # Parameters for animation
        self._past_data = []
        self._anim_data = []
        self._tpts      = []
        self._ANIMATION_INTERVAL = 25   # Frame rate for animation

        # Storage for all the line plots
        self._lines     = []

    def _initAnimationFrame(self):
        """
        _initAnimationFrame(self)
        Local function used for initializing the animation frame

        :returns: Line object which should be plotted in the first animation
            frame
        """

        min_x = np.inf
        max_x = -np.inf
        min_y = np.inf
        max_y = -np.inf

        for idx, line in enumerate(self._lines):
            min_x = min(min_x, min(self._anim_data[idx][0]))
            max_x = max(max_x, max(self._anim_data[idx][0]))

            min_y = min(min_y, min(self._anim_data[idx][1]))
            max_y = max(max_y, max(self._anim_data[idx][1]))

        # print("Setting Axes limits: (", min_x, ",", max_x, "), (", min_y, ",", max_y, ")")
        self._axes.set_xlim(min_x, max_x)
        self._axes.set_ylim(min_y, max_y)

        # TODO: Set the limits for Z coordinate

        return self._nextAnimationFrame()

    def _nextAnimationFrame(self, step=0):
        """
        _nextAnimationFrame(self, step)
        Local function used for animations of trajectories. If no value for
        'step' or the frame index is provided, this returns the first frame
        (default). It can therefore be used for the initial frame too

        :step: The index of the step or frame at which the system is
        :returns: A Line object which should be plotted at the next animation
            frame
        """

        # print("Setting up next frame")

        for idx, anim_data in enumerate(self._anim_data):
            # This loop enumerates each trajectory
            # Now within each trajectory, we need to enumerate each dimension
            for dim, dim_data in enumerate(anim_data):
                self._past_data[idx][dim] += [dim_data[step]]

        self._update()
        return self._lines

    def animate(self, tr_obj):
        """
        animate(self, tr_obj)
        Function that plots time-value data as animations in 1, 2 or 3
        dimensions.

        :tr_obj: The trajectory object that has to be animated. This can be a
            single 1, 2, or 3 dimensional trajectory or a collection of several
            of these in a TrajectorySet container
        """

        # FuncAnimation is the animation type where a function is repeatedly
        # called to create the next frame. The other options that can be used
        # for animation (Keep in mind for future use) are:
        # 1. TimedAnimation (Superclass of FuncAnimation)
        # 2. ArtistAnimation (Entire animation is recorded in the form of
        #   Artists already and is just replayed)

        n_trajectories  = tr_obj.getNTrajectories()
        tpts            = tr_obj.getTPts()

        n_frames        = len(tpts)

        self._tpts      = tpts
        self._anim_data = []
        self._past_data = []

        for traj in range(n_trajectories):
            self._anim_data.append([])
            self._past_data.append([])
            for arg in tr_obj.getSampleValues(traj):
                self._anim_data[traj].append(arg)
                self._past_data[traj].append([])

        # print(self._anim_data)

        # Set up the line plots for animation
        # print("Animating", n_trajectories, "trajectories, and", n_frames, "frames.")
        self._lines     = [[] for traj in range(n_trajectories)]
        for traj in range(n_trajectories):
            self._lines[traj],    = pl.plot([], [], animated=True)

        # TODO: Setting blit to True causes the initialization function to be
        # called twice instead of just one time, strange. Setting it to false,
        # however, stops all plotting.
        anim = animation.FuncAnimation(self._figure, self._nextAnimationFrame, np.arange(0, n_frames), \
                init_func=self._initAnimationFrame, interval=self._ANIMATION_INTERVAL, blit=True, \
                repeat=False)

        pl.show()


    def _update(self):
        """
        _update(self)
        Local function used to update an exisiting set of line plots. We can
        append the data in self._past_data to the existing line plots

        :returns: Line object which can be used by matplotlib's animation
            module
        """

        # Make sure that we have the correct number of line plots being fed in
        # as we already have in the current plot.
        # assert(len(self._lines) == len(plt_args))

        for idx, line in enumerate(self._lines):
            line.set_data(*self._past_data[idx])

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
