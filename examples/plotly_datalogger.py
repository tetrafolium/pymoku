from pymoku import Moku, MokuException
from pymoku.instruments import *

import pymoku.plotly as pmp

import time, logging, traceback

logging.basicConfig(format='%(asctime)s:%(name)s:%(levelname)s::%(message)s')
logging.getLogger('pymoku').setLevel(logging.DEBUG)

# Use Moku.get_by_serial() or get_by_name() if you don't know the IP
m = Moku.get_by_name('example')

i = m.discover_instrument()

if i is None or i.type != 'oscilloscope':
	print "No or wrong instrument deployed"
	i = Oscilloscope()
	m.attach_instrument(i)
else:
	print "Attached to existing Oscilloscope"

try:
i.set_defaults()
i.set_samplerate(10)
i.set_xmode(OSC_ROLL)
i.commit()

if i.datalogger_busy():
	i.datalogger_stop()

pmp.init(m, 'benizl.anu', 'na8qic5nqw', 'kdi5h54dhl', 'v7qd9o6bcq')

i.datalogger_start(start=0, duration=60*10, filetype='plot')

print "Plotly URL is: %s" % pmp.url(m)

	while True:
		time.sleep(1)
		trems, treme = i.datalogger_remaining()
		samples = i.datalogger_samples()
		print "Captured (%d samples); %d seconds from start, %d from end" % (samples, trems, treme)
		# TODO: Symbolic constants
		if i.datalogger_completed():
			break

	e = i.datalogger_error()

	if e:
		print "Error occured: %s" % e

	i.datalogger_stop()
	i.datalogger_upload()

except Exception as e:
	print e
finally:
	i.datalogger_stop()
	m.close()
