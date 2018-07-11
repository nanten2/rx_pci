#!/usr/bin/env python3

import os
import sys
import numpy
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot

target = sys.argv[1]
basedir = os.path.dirname(target)
fname = os.path.basename(target)
saveto = os.path.join(basedir, 'fig', fname+'.png')

print('target: {target}'.format(**locals()))



d = numpy.loadtxt(target)[1:]
t0 = d[0,0]
t = (d[:,0] - t0) / 60
dewar_temp = d[:,1]
powermeter = d[:,2]
sis_v1 = d[:,3]
sis_i1 = d[:,4]
sis_v2 = d[:,5]
sis_i2 = d[:,6]

# --
matplotlib.rcParams['font.size'] = 9
matplotlib.rcParams['font.family'] = 'freesans'
matplotlib.rcParams['xtick.top'] = True
matplotlib.rcParams['xtick.bottom'] = True
matplotlib.rcParams['xtick.direction'] = 'in'
matplotlib.rcParams['xtick.minor.visible'] = True
matplotlib.rcParams['ytick.left'] = True
matplotlib.rcParams['ytick.right'] = True
matplotlib.rcParams['ytick.direction'] = 'in'
matplotlib.rcParams['ytick.minor.visible'] = True


fig = matplotlib.pyplot.figure(figsize=(10,7))
ax = [fig.add_subplot(2,3,i+1) for i in range(6)]
ax[0].plot(t, dewar_temp, '-')
ax[3].plot(t, powermeter, '-')
ax[1].plot(t, sis_v1, '-')
ax[2].plot(t, sis_i1, '-')
ax[4].plot(t, sis_v2, '-')
ax[5].plot(t, sis_i2, '-')

ax[0].set_title('Dewar temp. (K)')
ax[3].set_title('Power meter (dBm)')
ax[1].set_title('SIS-1 V (mV)')
ax[2].set_title('SIS-1 I (uA)')
ax[4].set_title('SIS-2 V (mV)')
ax[5].set_title('SIS-2 I (uA)')

[a.grid(True, linestyle=':') for a in ax]
[a.set_xlabel('Time (min.)') for i, a in enumerate(ax) if i/3>=1]

fig.suptitle('save_logger_low : '+fname) 
fig.savefig(saveto)
