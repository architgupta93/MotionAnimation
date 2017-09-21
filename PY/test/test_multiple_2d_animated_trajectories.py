from MotionAnimation.PY import graphics as grp
from MotionAnimation.PY import data_types as mtype
import numpy as np

tstart  = -1.0
tstop   = 1.0

n_pts   = 100
tpts    = np.linspace(tstart, tstop, n_pts)

# Some random test functions for generating XY data
xvals   = pow(tpts, 2) * np.sin(np.pi * tpts)
yvals   = -2.0 * tpts * np.cos(np.pi * tpts)

# Bundle the data together in a Trajectory
xy_tr   = mtype.Trajectory__2D(tpts, xvals, yvals)

# Add another trajectory to the plot. This one has a different number of time
# points, say more finely sampled in the same range

n_pts2  = 100
tpts2   = np.linspace(tstart, tstop, n_pts2)

# Another test trajectory constructed with the new time points
xvals2  = 2.0 * tpts2 * np.cos(np.pi * tpts2)
yvals2  = np.tanh(tpts2) * np.sin(np.pi * tpts2)

# Putting these together in a trajectory set
tr_cls  = mtype.getTRClass(2)
xy_tr2  = mtype.Trajectory__2D(tpts2, xvals2, yvals2)

tr_set  = mtype.TrajectorySet()
tr_set.append(xy_tr)
tr_set.append(xy_tr2)

tr_set.plotTimedTR()
