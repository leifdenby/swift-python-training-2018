# -*- coding: utf-8 -*-

import os
import numpy as np
from tqdm import tqdm
import termcolor
import time
import datetime


def is_up(ip):
    response = os.system("ping -c 1 -w 2 " + ip + " > /dev/null 2>&1")

    if response == 0:
        return True
    else:
        return False

hosts = [
    ('internet', '8.8.8.8'),
    ('GSSTI-headnode', '192.168.169.250')
]

def get_state_for_print(ip):
    if is_up(ip):
        return termcolor.colored('✔', 'green')
    else:
        return termcolor.colored("x", 'red')

while True:
    time.sleep(0.4)
    print()
    state = {}
    for (host, ip) in hosts:
        state[host] = get_state_for_print(ip)

    os.system('clear')
    print("Internet status {}:\n".format(datetime.datetime.now()), )
    for (host, state) in state.items():
        print("\t{}: {}\n".format(host, state))
