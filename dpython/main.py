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
from os import path
from os.path import realpath, dirname, isfile, isdir
from subprocess import Popen
from typing import Tuple


def _recognize_file(argv) -> Tuple[str, int]:
    # todo: use importlib or something to find entry file reliably

    i = 1
    for arg in argv:
        if '-' not in arg:

            if '.' in arg and isfile(arg.replace('.', path.sep) + '.py'):
                return arg.replace('.', path.sep) + '.py', i

            if not arg.endswith('.py'):
                if isdir(arg):
                    if isfile(path.join(arg, '__init__.py')) and isfile(path.join(arg, '__main__.py')):
                        arg = path.join(arg, '__main__.py')
                        return arg, i
                elif isfile(arg + '.py'):
                    return arg + '.py', i
            else:
                return arg, i
        i += 1

    raise Exception("can't locate entry script")


def cmd():
    parser = argparse.ArgumentParser()

    parser.add_argument('args',
                        help='Provide `dpython config path/to/startup.py` to load startup script, otherwise the same as python command line. try  `dpython -- blahblah` if your blahblah contains dashed flags, e.g. `dpython -- -m folder`',
                        nargs='*')

    args = parser.parse_args().args

    print(args)
    if len(args) >= 2:

        if args[0] == 'config':

            thing = args[1]

            assert thing, 'please provide a command: `clear-script`|`clear-package`|`inspect-script`|`inspect-package` python script or package folder'

            if thing == 'clear-script':
                pass
            elif thing == 'clear-package':
                pass
            elif thing == 'inspect-script':
                with open(path.join(dirname(__file__), 'config.py'), 'r') as config_cache_file:
                    print(config_cache_file.read())
                return
            elif thing == 'inspect-package':
                pass
            else:

                with open(thing) as new_config_file:
                    config_script = new_config_file.read() + '\n'
                with open(path.join(dirname(__file__), 'config.py'), 'w') as config_cache_file:
                    config_cache_file.write(config_script)

                print('new startup script configured')
                return

    with open(path.join(dirname(__file__), 'config.py'), 'r') as config_cache_file:
        config_script = config_cache_file.read()

    if not args:  # interactive shell
        with tempfile.NamedTemporaryFile(mode='r+', suffix='.py', dir='.') as fake_script_file:
            fake_script_file.write(config_script)
            fake_script_file.seek(0)
            command = ['python3', '-i', fake_script_file.name]
            print(command)

            p = Popen(command)
            p.wait()
    else:
        # todo: read idioms and be less cringy
        if sys.argv[1] == '--':
            file, ind = _recognize_file(sys.argv[2:])
        else:
            file, ind = _recognize_file(sys.argv[1:])

        # fool proof
        if file.endswith('config.py') and not isfile(file):
            print("Can't find config.py or package config, did you mean [config] [script-path]?", file=sys.stderr)
            return
        with open(file) as script_file:
            script = script_file.read()

        # print(script)

        with tempfile.NamedTemporaryFile(mode='r+', suffix='.py', dir=dirname(realpath(file))) as fake_script_file:
            fake_script_file.write(config_script + '\n')
            fake_script_file.write(script)
            fake_script_file.seek(0)
            sys.argv[ind] = fake_script_file.name
            command = ['python3'] + sys.argv[1:]
            print(command)

            p = Popen(command)
            p.wait()
