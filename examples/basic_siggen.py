from pymoku import Moku, ValueOutOfRangeException
from pymoku.instruments import *
import time, logging

import matplotlib
import matplotlib.pyplot as plt

logging.basicConfig(format='%(asctime)s:%(name)s:%(levelname)s::%(message)s')
logging.getLogger('pymoku').setLevel(logging.DEBUG)

# Use Moku.get_by_serial() or get_by_name() if you don't know the IP
m = Moku.get_by_name("Aqua")

i = m.discover_instrument()

if i is None or i.type != 'signal_generator':
	print "No or wrong instrument deployed"
	i = SignalGenerator()
	m.attach_instrument(i)
else:
	print "Attached to existing Signal Generator"

i.set_defaults()

i.synth_sinewave(1, 1.0, 1000000)
i.synth_squarewave(2, 1.0, 2000000, risetime=0.1, falltime=0.1, duty=0.3)
i.commit()

try:
	while True:
		try:
			i.out1_offset += 0.05
		except ValueOutOfRangeException:
			i.out1_offset = -1

		print i.out1_offset

		i.commit()
finally:
	m.close()
