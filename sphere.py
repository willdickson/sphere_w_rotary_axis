from __future__ import print_function
import os 
import sys
from py2gcode import gcode_cmd
from py2gcode import cnc_dxf

feedrate = 0.4*0.10
depth_per_360 = 0.4*0.03

zero_pos = {'x': 0.0, 'y': 0.0, 'z': 0.0, 'a': 0.0}
start_pos = {'x': 0.0, 'y': 0.0, 'z': 0.0, 'a': 0.0}
final_pos = {'x': 0.0, 'y': 0.0, 'z': -0.6}

#start_pos = {'x': 0.0, 'y': 0.0, 'z': -0.5, 'a': 0.0}
#final_pos = {'x': 0.0, 'y': 0.0, 'z': -0.9}
final_pos['a'] = 360*abs(final_pos['z']-start_pos['z'])/depth_per_360

total_t = abs(final_pos['z'] - start_pos['z'])/feedrate
angle_rate = abs(final_pos['a'] - start_pos['a'])/total_t
print('start_pos: ', start_pos)
print('final_pos: ', final_pos)
print('total_t: ', total_t)
print('angle_rate: ', angle_rate)


prog = gcode_cmd.GCodeProg()
prog.add(gcode_cmd.GenericStart())
prog.add(gcode_cmd.Space())
prog.add(gcode_cmd.FeedRate(feedrate))

prog.add(gcode_cmd.RapidMotion(**start_pos))
prog.add(gcode_cmd.LinearFeed(**final_pos))
del zero_pos['a']
prog.add(gcode_cmd.RapidMotion(**zero_pos))

prog.add(gcode_cmd.Space())
prog.add(gcode_cmd.End(),comment=True)
baseName, dummy = os.path.splitext(__file__)
fileName = '{0}.ngc'.format(baseName)
print('generating: {0}'.format(fileName))
prog.write(fileName)
