from MotionAnimation.PY import graphics as grp
from MotionAnimation.PY import data_types as mtype
import numpy as np

tstart  = 0.0
tstop   = 1.0

n_pts   = 100
tpts    = np.linspace(tstart, tstop, n_pts)

# Some random test functions for generating XY data
xvals   = pow(tpts, 2) * np.sin(np.pi * tpts)
yvals   = -2.0 * tpts * np.cos(np.pi * tpts)

# Bundle the data together in a Trajectory
xy_tr   = mtype.Trajectory__2D(tpts, xvals, yvals)
xy_tr.plotTimedTR()
