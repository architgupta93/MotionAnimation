from MotionAnimation.PY import data_types as mtype
import numpy as np


# First trajectory to be plotted
n_pts   = 100
tpts    = np.linspace(0.0, 1.0, n_pts)
xvals   = pow(tpts, 2) * np.sin(np.pi * tpts)
yvals   = -2.0 * tpts * np.cos(np.pi * tpts)

# Bundle the data together in a Trajectory
xy_tr   = mtype.Trajectory__2D(tpts, xvals, yvals)

# Add another trajectory to the plot
tr_set = mtype.TrajectorySet()
tr_set.append(xy_tr)

# Second trajectory to be plotted
tpts2   = np.linspace(-1.0, 1.0, 2 * n_pts)
xvals2  = 2.0 * tpts2 * np.cos(np.pi * tpts2)
yvals2  = np.tanh(tpts2) * np.sin(np.pi * tpts2)

# Let's see if we can get the correct constructor at runtime
tr_class= mtype.getTRClass(2) 
xy_tr2  = tr_class(tpts2, xvals2, yvals2)
tr_set.append(xy_tr2)

tr_set.plotStaticTR()
