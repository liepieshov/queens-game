#!/usr/bin/env python3
import signal

import time
import subprocess
import os

def read_file(fname: str) -> str:
    with open(fname, "r") as fd:
        return fd.read()

def watch_kill(fname: str, cmd: str) -> str:
    content = read_file(fname)
    pro = None
    pro = subprocess.Popen(cmd, stdout=subprocess.PIPE, 
                       shell=True, preexec_fn=os.setsid) 

    try:
        while True:
            time.sleep(3)
            new_content = read_file(fname)
            if new_content != content:
                content = new_content
                os.killpg(os.getpgid(pro.pid), signal.SIGTERM)
                pro = None
                pro = subprocess.Popen(cmd, stdout=subprocess.PIPE, 
                                   shell=True, preexec_fn=os.setsid) 
    finally:
        if pro is not None:
            os.killpg(os.getpgid(pro.pid), signal.SIGTERM)


def always_restart(cmd: str) -> str:
    while True:
        os.system(cmd)
        time.sleep(2)

if __name__ == '__main__':
    # watch_kill("game_gui.py", "python game_gui.py")
    always_restart( "python game_gui.py")
