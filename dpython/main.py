import io
import os
import sys
import select
import tempfile
import termios
import time
import tty
import pty
import argparse
from os.path import realpath, dirname
from subprocess import Popen
from typing import Tuple


def _recognize_file(argv) -> Tuple[str, int]:
    i = 1
    for arg in argv:
        if '-' not in argv:
            if not arg.endswith('.py'):
                arg += '.py'
            return arg, i
        i += 1


def cmd():
    parser = argparse.ArgumentParser()

    parser.add_argument('args', help='the same as python', nargs='+')

    file, ind = _recognize_file(sys.argv[1:])

    with open(file) as script_file:
        script = script_file.read()

    print(script)

    with open('/home/matt/PycharmProjects/dark-python/dpython/default_config.py') as config_file:
        config_script = config_file.read()

    with tempfile.NamedTemporaryFile(mode='r+', suffix='.py', dir=dirname(realpath(file))) as fake_script_file:
        fake_script_file.write(config_script + '\n')
        fake_script_file.write(script)
        fake_script_file.seek(0)
        sys.argv[ind] = fake_script_file.name
        command = ['python3'] + sys.argv[1:]
        print(command)


        p = Popen(command)
        p.wait()
