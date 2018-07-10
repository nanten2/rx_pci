import sys
sys.path.append('../scripts')
import stop_logger
import nasco_sisbb_contoroller

log = stop_logger()
ctrl = nasco_sisbb_contoroller()

initial_voltage = 0 # mV
final_voltage = 7 # mV
step = 0.1 # mV
roop = int((final_voltage - initial_voltage) / step)

for i in range(roop+1):
    ctrl.nasco_sisbb_set_voltage(ch=1, voltage=i*step)
    ctrl.nasco_sisbb_set_voltage(ch=2, voltage=i*step)

log.stop_logger()    

