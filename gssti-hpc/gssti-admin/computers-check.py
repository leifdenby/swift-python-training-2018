# -*- coding: utf-8 -*-

import os
import numpy as np
from tqdm import tqdm
import termcolor


def is_up(ip):
    response = os.system("ping -c 1 -w 1 " + ip + " > /dev/null 2>&1")

    if response == 0:
        return True
    else:
        return False


class State:
    OFFLINE = 0
    ONLINE = 1
    DOESNT_EXIST = -1
    FAULTY = -2

addresses = -1*np.ones((4, 6), dtype=int)

addresses[0, 0] = 35
addresses[0, 2] = 69
addresses[0, 4] = 70
addresses[0, 5] = 92

addresses[1, 0] = 65
addresses[1, 1] = 123
addresses[1, 2] = 49
addresses[1, 3] = 74
addresses[1, 4] = 47

addresses[2, 0] = 48
addresses[2, 1] = 15
addresses[2, 2] = 122
addresses[2, 3] = 87
addresses[2, 4] = 121
addresses[2, 5] = 120

addresses[3, 4] = 30
addresses[3, 5] = 96

states = State.DOESNT_EXIST*np.ones(addresses.shape, dtype=int)
states[0,1] = State.FAULTY
states[0,3] = State.FAULTY

print("Pinging workstations...")
for add in tqdm(addresses.flatten()):
    if add == -1:
        continue

    full_addr = "192.168.169.{}".format(add)
    i, j = np.where(addresses == add)

    if is_up(full_addr):
        states[i,j] = State.ONLINE
    else:
        states[i,j] = State.OFFLINE


nx, ny = addresses.shape

print("GSSTI worstations:\n")

for i in range(nx):
    for j in range(ny):
        state = states[i,j]
        state_str = None

        if state == State.ONLINE:
            state_str = termcolor.colored('✔', 'green')
        elif state == State.OFFLINE:
            state_str = termcolor.colored("x", 'red')
        elif state == State.DOESNT_EXIST:
            state_str = None
        elif state == State.FAULTY:
            state_str = termcolor.colored('f', 'white')
        else:
            state_str = termcolor.colored('?', 'yellow')

        if state_str is not None:
            print("[{}] ".format(state_str), end='')
        else:
            print("    ", end='')
    print()
    print()
