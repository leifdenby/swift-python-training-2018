#!/usr/bin/env python
from ecmwfapi import ECMWFDataServer

from datetime import datetime
import os

## Defining variables, time-span etc

OUTPUT_FILENAME = "ei_surface.nc"

area = (45, -25, -5, 50)  # (N, W, S, E)
t_start = datetime(2006, 7, 30, 18, 0, 0)
t_end = datetime(2006, 8, 2, 0, 0, 0)
params = "sp msl tcw tcwv 10u 10v 2t 2d lcc mcc hcc sm1 sm2 sm3 sm4".split()

# Dictionary mapping parameter short names to codes
# See http://apps.ecmwf.int/codes/grib/param-db
param_dict = {
    # Surface (sfc), available at step=0 and step=3 etc
    'sp': '134',  # surface pressure
    'tcw': '136',  # total column water
    'tcwv': '137',  # total column water vapor
    'msl': '151',  # mean sea level pressure
    'tcc': '164',  # total cloud cover
    '10u': '165',  # 10 metre U wind component
    '10v': '166',  # 10 meter V wind component
    '2t': '167',  # 2 metre temperature
    '2d': '168',  # 2 metre dewpoint temperature
    'lcc': '186',  # low cloud cover
    'mcc': '187',  # medium cloud cover
    'hcc': '188',  # high cloud cover
    'sm1': '39',  # soil moisture level 1
    'sm2': '40',  # soil moisture level 2
    'sm3': '41',  # soil moisture level 3
    'sm4': '42',  # soil moisture level 4
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
        'target': OUTPUT_FILENAME,
        'param': params_str,
        'levtype': 'sfc',
    }

    server.retrieve(req)
