from MotionAnimation.PY import data_types as mtype
import numpy as np

n_pts   = 100
tpts    = np.linspace(0.0, 1.0, n_pts)

# Some random test functions for generating XY data
xvals   = pow(tpts, 2) * np.sin(np.pi * tpts)
yvals   = -2.0 * tpts * np.cos(np.pi * tpts)

# Bundle the data together in a Trajectory
xy_tr   = mtype.Trajectory__2D(tpts, xvals, yvals)
xy_tr.plotStaticTR()
