#!/usr/bin/env python
#
# Modified from the version at
# https://gist.githubusercontent.com/ei-grad/4d9d23b1463a99d24a8d/raw/rotate.py
#
#

from time import sleep
from os import path as op
import sys
from subprocess import check_call, check_output
from glob import glob


def bdopen(fname):
    return open(op.join(basedir, fname))


def read(fname):
    return bdopen(fname).read()


for basedir in glob('/sys/bus/iio/devices/iio:device*'):
    if 'accel' in read('name'):
        break
else:
    sys.stderr.write("Can't find an accellerator device!\n")
    sys.exit(1)


devices = check_output(['xinput', '--list', '--name-only']).splitlines()

touchscreen_names = [b'FTSC1000:00 2808:1015']
touchscreens = [i.decode() for i in devices if any(j.lower() == i.lower() for j in touchscreen_names)]

disable_touchpads = False
'''
There's no value in trying to disable the touchpad when the tablet is disconnected
it just causes exceptions

touchpad_names = [b'touchpad', b'trackpoint']
touchpads = [i for i in devices if any(j in i.lower() for j in touchpad_names)]
'''

scale = float(read('in_accel_scale_available').split(" ")[0])

g = 7.0  # (m^2 / s) sensibility, gravity trigger

STATES = [
    {'rot': 'normal', 'coord': '1 0 0 0 1 0 0 0 1', 'touchpad': 'enable',
     'check': lambda x, y: y <= -g},
    {'rot': 'inverted', 'coord': '-1 0 1 0 -1 1 0 0 1', 'touchpad': 'disable',
     'check': lambda x, y: y >= g},
    {'rot': 'left', 'coord': '0 -1 1 1 0 0 0 0 1', 'touchpad': 'disable',
     'check': lambda x, y: x >= g},
    {'rot': 'right', 'coord': '0 1 0 -1 0 1 0 0 1', 'touchpad': 'disable',
     'check': lambda x, y: x <= -g},
]

# mapping
#
# lambdas have been swapped from -> to:
#
# inverted -> right
# normal -> left
# right -> inverted
# left -> normal
#
# Coords for left and right needed to be switched


STATES = [
    {'rot': 'normal', 'coord': '1 0 0 0 1 0 0 0 1', 'touchpad': 'enable',
     'check': lambda x, y: x >= g},
    {'rot': 'inverted', 'coord': '-1 0 1 0 -1 1 0 0 1', 'touchpad': 'disable',
     'check': lambda x, y: x <= -g},
    {'rot': 'left', 'coord': '0 -1 1 1 0 0 0 0 1', 'touchpad': 'disable',
     'check': lambda x, y: y <= -g},
    {'rot': 'right', 'coord': '0 1 0 -1 0 1 0 0 1', 'touchpad': 'disable',
     'check': lambda x, y: y >= g},
]



def rotate(state):
    s = STATES[state]
    check_call(['xrandr', '-o', s['rot']])
    for dev in touchscreens:
        #print(f'Configuring {dev}')
        check_call([
            'xinput', 'set-prop', dev,
            'Coordinate Transformation Matrix',
        ] + s['coord'].split())
    '''
    if disable_touchpads:
        for dev in touchpads:
            check_call(['xinput', s['touchpad'], dev])
    '''

def read_accel(fp):
    fp.seek(0)
    return float(fp.read()) * scale


if __name__ == '__main__':

    accel_x = bdopen('in_accel_x_raw')
    accel_y = bdopen('in_accel_y_raw')

    current_state = None
    while True:
        x = read_accel(accel_x)
        y = read_accel(accel_y)
        for i in range(4):
            if i == current_state:
                continue
            if STATES[i]['check'](x, y):
                #print(STATES[i]['rot'])
                current_state = i
                rotate(i)
                break
        sleep(0.5)
