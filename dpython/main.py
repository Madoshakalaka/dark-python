import glob
import os
import sys
import tempfile
from os import path
from os.path import realpath, dirname, isfile, isdir
from pathlib import Path
from subprocess import Popen
from typing import Tuple, Union


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


def _dir_is_package(directory: Union[Path, str]):
    return isfile(path.join(directory, '__init__.py'))


def cmd():
    args = sys.argv[1:]

    if len(args) == 1 and args[0] in ['-h', '--help']:
        print("""
To configure startup scripts, custom packages:
usage: dpython [-h]
       {config}
       {clear-script,clear-package,inspect-script,inspect-package}

Otherwise, just use dpython as python command line, 'python3 -h' to see help for example
""")
        return
    script_path = path.join(dirname(__file__), 'config.py')
    if not isfile(script_path):
        print('')
        return

    if len(args) >= 2:

        if args[0] == 'config':

            thing = args[1]

            if thing == 'clear-script':
                with open(path.join(dirname(__file__), 'config.py'), 'w') as _:
                    pass
                print('start up script cleared')
                return
            elif thing == 'clear-package':
                priority_dir = path.join(dirname(__file__), 'priority_packages')
                for i in glob.glob(path.join(priority_dir, '*')):
                    print(path.split(i)[-1], 'removed')
                    os.unlink(i)
                return
            elif thing == 'inspect-script':
                script_path = path.join(dirname(__file__), 'config.py')
                if not isfile(script_path):
                    print('')
                    return

                with open(script_path, 'r') as config_cache_file:
                    print(config_cache_file.read())
                return
            elif thing == 'inspect-package':
                print('patch packages:')
                priority_dir = path.join(dirname(__file__), 'priority_packages')
                for i in glob.glob(path.join(priority_dir, '*')):
                    print(path.split(i)[-1])
                return
            else:
                if isfile(thing):
                    with open(thing) as new_config_file:
                        config_script = new_config_file.read() + '\n'
                    with open(path.join(dirname(__file__), 'config.py'), 'w') as config_cache_file:
                        config_cache_file.write(config_script)

                    print('new startup script configured')
                    return
                elif isdir(thing):

                    if _dir_is_package(thing):

                        priority_dir = path.join(dirname(__file__), 'priority_packages')
                        if not isdir(priority_dir):
                            os.mkdir(priority_dir)

                        os.symlink(path.realpath(thing), path.join(priority_dir, path.split(thing)[-1]),
                                   target_is_directory=True)

                        print("patch package configured")
                        return

                raise Exception('neither python file nor python package is provided')

    with open(path.join(dirname(__file__), 'config.py'), 'r') as config_cache_file:
        config_script = config_cache_file.read()

    if not args:  # interactive shell
        with tempfile.NamedTemporaryFile(mode='r+', suffix='.py', dir='.') as fake_script_file:
            fake_script_file.write(
                "import sys\nsys.path.insert(0, '%s')\n" % path.join(dirname(__file__), 'priority_packages'))

            fake_script_file.write(config_script)
            fake_script_file.seek(0)
            command = [sys.executable, '-i', fake_script_file.name]
            print(command)

            p = Popen(command)
            p.wait()
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
            fake_script_file.write(
                "import sys\nsys.path.insert(0, '%s')\n" % path.join(dirname(__file__), 'priority_packages'))
            fake_script_file.write(config_script + '\n')
            fake_script_file.write(script)
            fake_script_file.seek(0)
            if '-m' in sys.argv or '--module' in sys.argv:
                pass
            else:
                sys.argv[ind] = fake_script_file.name
            command = [sys.executable] + sys.argv[1:]

            p = Popen(command)
            p.wait()
