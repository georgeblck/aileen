import subprocess
import os


def syscmd(cmd, waiting=False):
    DEVNULL = open(os.devnull, 'wb')
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
                         stdout=DEVNULL, stderr=subprocess.STDOUT)
    if waiting:
        p.wait()
