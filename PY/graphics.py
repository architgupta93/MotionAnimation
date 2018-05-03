import matplotlib.pylab as pl
import matplotlib.cm as colormap
import matplotlib.animation as animation
import numpy as np

from mpl_toolkits.mplot3d import Axes3D

class GraphicsContainer(object):
    """
    Parent object for storing graphical structures.  The information stored in
    this object is used for rendering both static and dynamic plots
    """

    TEXT_FONT_SIZE      = 20

    def __init__(self, axes_projection=None):
        """
        Class constructor
        :axes_projection: In case a 3D plot is required, axes can be set up for
            it by passing the argument '3d' as axes_projection
        """

        # Before plotting anything, update the appropriate font sizes. This
        # should probably be done in the __init__ file: TODO
        pl.rcParams.update({'font.size':GraphicsContainer.TEXT_FONT_SIZE})

        # By default, we have 2D axes.
        self._figure    = pl.figure()     
        self._axes      = pl.axes(projection=axes_projection)
        self._is_3d     = (axes_projection == '3d')
        self._x_label   = 'x'
        self._y_label   = 'y'
        self._z_label   = 'z'

        # Some paratmeters for plotting
        self._line_width    = 3.0

        # Include a pointer to the trajectory object
        self._tr_obj    = []

        # Parameters for animation
        self._past_data = []
        self._anim_data = []
        self._tpts      = []
        self._t_elapsed = []
        self._ANIMATION_INTERVAL = 25   # Frame rate for animation

        # Storage for all the line plots
        self._track     = []

    def _initAnimationFrame(self):
        """
        _initAnimationFrame(self)
        Local function used for initializing the animation frame

        :returns: Line object which should be plotted in the first animation
            frame
        """

        # We require that all trajectories should start at the same time. While
        # the exact t0 values might not be identical because of finite
        # precision arithmetic, all t0 values should be smaller than all t1
        # values
        # TODO: Check this here

        min_x = np.inf
        max_x = -np.inf
        min_y = np.inf
        max_y = -np.inf

        for idx, _ in enumerate(self._track):
            min_x = min(min_x, min(self._anim_data[idx][0]))
            max_x = max(max_x, max(self._anim_data[idx][0]))

            min_y = min(min_y, min(self._anim_data[idx][1]))
            max_y = max(max_y, max(self._anim_data[idx][1]))

        # print("Setting Axes limits: (", min_x, ",", max_x, "), (", min_y, ",", max_y, ")")
        self._axes.set_xlim(min_x, max_x)
        self._axes.set_ylim(min_y, max_y)

        # TODO: Set the limits for Z coordinate

        return self._nextAnimationFrame()

    def _setupTracks(self, n_trajectories):
        """TODO: Docstring for _setupTracks.
        :returns: TODO

        """
        for traj in range(n_trajectories):
            self._track[traj] = None

    def _nextAnimationFrame(self):
        """
        Default implementation, not to be used.
        Protected function for creating the next animation frame.

        """

        return None

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

        self._tpts      = [tr_obj.getTPts(traj) for traj in range(n_trajectories)]

        # t_elapsed stores the index of the last time point that elapsed for
        # the animation frame
        self._t_elapsed = [0 for traj in range(n_trajectories)]

        # This gets the time points for the first trajectory. By default, this
        # serves as the reference time
        n_frames        = len(self._tpts[0])

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
        self._track = [[] for traj in range(n_trajectories)]
        self._setupTracks(n_trajectories)

        # TODO: Setting blit to True causes the initialization function to be
        # called twice instead of just one time, strange. Setting it to false,
        # however, stops all plotting.
        anim = animation.FuncAnimation(self._figure, self._nextAnimationFrame, np.arange(0, n_frames), \
                init_func=self._initAnimationFrame, interval=self._ANIMATION_INTERVAL, blit=True, \
                repeat=False)

        pl.show()

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

        # Set up the line widths and fonts for axes labels
        for line in self._track:
            line.set_linewidth(self._line_width)

        # Display the plot
        # pl.ion()
        pl.show(self._axes)

    def getFigureWindow(self):
        return self._figure

class LineContainer(GraphicsContainer):
    """
    Derived from GraphicsContainer for specifically animating Line or line-like
    objects. At any point in the animation, the entire history of the line
    object is visible and the line keeps growing

    """

    def __init__(self, axes_projection=None):
        GraphicsContainer.__init__(self, axes_projection)

    def _setupTracks(self, n_trajectories):
        """TODO: Docstring for _setupTracks.
        :returns: TODO

        """

        # Choosing colors for different trajectories
        colors = colormap.magma(np.linspace(0, 1, n_trajectories))
        for traj in range(n_trajectories):
            self._track[traj],    = pl.plot([], [], animated=True, c=colors[traj])

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
        next_time_val_for_frame = self._tpts[0][step]
        # print("Searching for time point:", next_time_val_for_frame)

        for idx, anim_data in enumerate(self._anim_data):
            # This loop enumerates each trajectory
            # Now within each trajectory, we need to enumerate each dimension
            idx_step = np.searchsorted(self._tpts[idx], next_time_val_for_frame)
            # print("Time point: ", self._tpts[idx][idx_step], "found at index:", idx_step)
            for dim, dim_data in enumerate(anim_data):
                for frame_index in range(self._t_elapsed[idx], idx_step):
                    self._past_data[idx][dim].append(dim_data[frame_index])
            self._t_elapsed[idx] = idx_step

        self._update()
        return self._track

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
        # assert(len(self._track) == len(plt_args))

        for idx, line in enumerate(self._track):
            line.set_data(*self._past_data[idx])

    def plot(self, *plt_args):
        """
        plot(self, *plt_args)
        :*plt_args: Variable number of arguments to be plotted (Shouldn't be
        more that 3)
        :returns: Nothing is returned at the end of the function, however, the
            _track member of the class is updated with the line that was
            plotted
        """
        
        new_trajectories = self._axes.plot(*plt_args)
        for tr in new_trajectories:
            self._track.append(tr)
        return

class PointContainer(LineContainer):
    """
    Derived from LineContainer. This object shows the movement of an object
    in space. Only the current position (or a short, fixed trail is displayed)

    """

    def __init__(self, axes_projection=None):
        LineContainer.__init__(self, axes_projection)

    def _setupTracks(self, n_trajectories):
        """TODO: Docstring for _setupTracks.
        :returns: TODO

        """
        for traj in range(n_trajectories):
            self._track[traj],    = pl.plot([], [], animated=True, marker='o')

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
        next_time_val_for_frame = self._tpts[0][step]
        # print("Searching for time point:", next_time_val_for_frame)

        for idx, anim_data in enumerate(self._anim_data):
            # This loop enumerates each trajectory
            # Now within each trajectory, we need to enumerate each dimension
            idx_step = np.searchsorted(self._tpts[idx], next_time_val_for_frame)
            # print("Time point: ", self._tpts[idx][idx_step], "found at index:", idx_step)
            for dim, dim_data in enumerate(anim_data):
                for frame_index in range(self._t_elapsed[idx], idx_step):
                    self._past_data[idx][dim] = dim_data[frame_index]
            self._t_elapsed[idx] = idx_step

        self._update()
        return self._track