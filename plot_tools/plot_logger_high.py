#!/usr/bin/env python3

import os
import sys
import numpy
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot

target = sys.argv[1]
saveto1 = os.path.join(target, 'qlook-all.png')
saveto2 = os.path.join(target, 'qlook-iv.png')

print('target: {target}'.format(**locals()))


path_dewartemp = os.path.join(target, 'l218.txt')
path_powermeter = os.path.join(target, 'ml2437a.txt')
path_sisbb = os.path.join(target, 'sisbb.txt')

d_dewartemp = numpy.loadtxt(path_dewartemp)
d_powermeter = numpy.loadtxt(path_powermeter)
d_sisbb = numpy.loadtxt(path_sisbb)

t_dt = d_dewartemp[:,0]
dewar_temp = d_dewartemp[:,1]

t_pm = d_powermeter[:,0]
powermeter = d_powermeter[:,1]

t_sis = d_sisbb[:,0]
sis_v1 = d_sisbb[:,1]
sis_i1 = d_sisbb[:,2]
sis_v2 = d_sisbb[:,3]
sis_i2 = d_sisbb[:,4]

# --
matplotlib.rcParams['font.size'] = 9
matplotlib.rcParams['font.family'] = 'freesans'
# matplotlib.rcParams['xtick.top'] = True
# matplotlib.rcParams['xtick.bottom'] = True
matplotlib.rcParams['xtick.direction'] = 'in'
matplotlib.rcParams['xtick.minor.visible'] = True
# matplotlib.rcParams['ytick.left'] = True
# matplotlib.rcParams['ytick.right'] = True
matplotlib.rcParams['ytick.direction'] = 'in'
matplotlib.rcParams['ytick.minor.visible'] = True


fig = matplotlib.pyplot.figure(figsize=(10,7))
ax = [fig.add_subplot(2,3,i+1) for i in range(6)]
ax[0].plot(t_dt, dewar_temp, '-')
ax[3].plot(t_pm, powermeter, '-')
ax[1].plot(t_sis, sis_v1, '-')
ax[2].plot(t_sis, sis_i1, '-')
ax[4].plot(t_sis, sis_v2, '-')
ax[5].plot(t_sis, sis_i2, '-')

ax[0].set_title('Dewar temp. (K)')
ax[3].set_title('Power meter (dBm)')
ax[1].set_title('SIS-1 V (mV)')
ax[2].set_title('SIS-1 I (uA)')
ax[4].set_title('SIS-2 V (mV)')
ax[5].set_title('SIS-2 I (uA)')

[a.grid(True, linestyle=':') for a in ax]
[a.set_xlabel('Unix Time') for i, a in enumerate(ax) if i/3>=1]

fig.suptitle('save_logger_high : '+target) 
fig.savefig(saveto1)



fig = matplotlib.pyplot.figure(figsize=(10,7))
ax = [fig.add_subplot(2,3,i+1) for i in range(6)]
ax[0].plot(t_sis, sis_v1, '-')
ax[1].plot(t_sis, sis_i1, '-')
ax[2].plot(sis_v1, sis_i1, '.')
ax[3].plot(t_sis, sis_v2, '-')
ax[4].plot(t_sis, sis_i2, '-')
ax[5].plot(sis_v2, sis_i2, '.')

ax[0].set_title('SIS-1 V (mV)')
ax[1].set_title('SIS-1 I (uA)')
ax[2].set_title('SIS-1 I-V')
ax[3].set_title('SIS-2 V (mV)')
ax[4].set_title('SIS-2 I (uA)')
ax[5].set_title('SIS-2 I-V')

[a.grid(True, linestyle=':') for a in ax]
#[a.set_xlabel('V (mV)') for i, a in enumerate(ax) if i/3>=1]

fig.suptitle('save_logger_high : '+target) 
fig.savefig(saveto2)
