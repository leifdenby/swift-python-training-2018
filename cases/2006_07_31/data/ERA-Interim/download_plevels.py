#!/usr/bin/env python
from ecmwfapi import ECMWFDataServer

from datetime import datetime
import os

## Defining variables, time-span etc

OUTPUT_FILENAME = "ei_model_levels.nc"

area = (45, -25, -5, 50)  # (N, W, S, E)
t_start = datetime(2006, 7, 30, 18, 0, 0)
t_end = datetime(2006, 8, 2, 0, 0, 0)
params = "u v w r vo q z t".split()

p_levels = "100/125/150/175/200/225/250/300/350/400/450/500/550/600/650/700/"\
           "750/775/800/825/850/875/900/925/950/975/1000",

## Build params string

# Dictionary mapping parameter short names to codes
# See http://apps.ecmwf.int/codes/grib/param-db
param_dict = {
    # Pressure levels (pl), eg 850, 500
    'z': '129',  # geopotential
    't': '130',  # temperature
    'u': '131',  # U component of wind
    'v': '132',  # V component of wind
    'q': '133',  # specific humidity
    'w': '135',  # vertical velocity
    'vo': '138',  # vorticity (relative)
    'r': '157',  # relative humidity
    'pt': '3',  # potential temperature
}

missing_params = list(filter(lambda p: p not in param_dict, params))
if len(missing_params) > 0:
    raise NotImplementedError("Please add `{}` to param_dict".format(
        ",".join(missing_params)
    ))
params_str = "/".join(["{}.128".format(param_dict.get(p)) for p in params])


DATE_FORMAT = '%Y-%m-%d'

if os.path.exists(OUTPUT_FILENAME):
    print("{} exists, skipping".format(OUTPUT_FILENAME))
else:
    server = ECMWFDataServer()
    req = {
        'class': 'ei',
        'dataset': 'interim',
        'date': '{}/to/{}'.format(
            t_start.strftime(DATE_FORMAT),
            t_end.strftime(DATE_FORMAT),
        ),
        'expver': '1',
        'grid': '0.75/0.75',
        'step': '0',
        'stream': 'oper',
        'format': 'netcdf',
        'type': 'an',
        'time': '00:00:00/06:00:00/12:00:00/18:00:00',
        'area': "{}/{}/{}/{}".format(*area),
        'levtype': 'pl',
        'levelist': p_levels,
        'param': params_str,
        'target': OUTPUT_FILENAME,
    }
    server.retrieve(req)
