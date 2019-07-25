# Dark Python
![travis-badge](https://travis-ci.org/Madoshakalaka/dark-python.svg?branch=master)

Patch python built-in functions and libraries!

Create your own python!

Do dangerous things in python you've never dreamed of!

## What it does

- patch built-in function

`$ dpython config beautify.py`

```python 
# beautify.py
from pprint import pprint
print = pprint
```
and just use `$ dpython` as python command line for the rest of your life, every `print` is guaranteed to be pretty.

- patch any package, built-in or not

`$ dpython config troll_packages/random`

```
random
└── __init__.py
```
```python
#__init__.py
def randint(a,b):
    return a
```

And now ssh into some production server. `$ sudo alias python3=dpython`  and watch the world burn.

## Use case

Combined with [the forbidden fruit](https://github.com/clarete/forbiddenfruit). You can do anything, including:

1. Customize your python however you like. Are you a data scientist who find it impossible to do anything with python vanilla list? No problem! Extend built-in list with numpy array functionality!

2. Patch a shit ton of python code without doing any refactoring

3. Create python **patch package** for other packages

## How to use

`pip install dpython`

By default, pip creates command line shortcut `$ dpython`. If it does not work, (You're using stupid Windows or something), you can always use `> python -m dpython`

`dpython` by itself works exactly the same as `python` command line.

e.g.:

`$ dpython test.py`  runs `test.py`

`$ dpython` opens interactive shell

`$ dpython -m my_module` runs folder `my_module` as a python module
#
dpython only has one reserved sub-command which is different from python: `'config'`. You can supply the following instructions:

`$ dpython config [something.py|folder]`. Register either a single `.py` file or a folder containing a python package.

- In the case of `py` file. The supplied file will effectively be executed prior to future `$ dpython` calls. You can call it a startup script.
- In the case of a package, imports in other code will use the supplied package instead of ones with duplicate names.
- You can register as many as packages as you like. But only one `.py` startup script.


`$ dpython config inspect-script` Print the saved startup script

`$ dpython config clear-script` Reset the saved startup script

`$ dpython config inspect-package` Print registered packages

```shell
# example output
patch packages:
random
numpy
argparse
```

`$ dpython config clear-package` Clear registered packages, won't delete real file.
```shell
# example output
random removed
numpy removed
argparse removed
```
`$ dpython -h|--help` to print help

## More Examples

- example 1

    ```python
    # leEtH4ck3r.py
    oldprint = print
    def print(*args, **kwargs):
        oldprint('Pwned  by Dark Python!!!')
        oldprint(*args, **kwargs)
    ```
    `$ dpython register leEtH4ck3r.py`

- example 2

    ```python
    # ilovetqdm.py
    from tqdm import trange
    range = trange
    ```
    `$ dpython register ilovetqdm.py`



## My Stupid Fantasies (todos)

- Write a package called `gwrap` that internally uses `dpython` to extend built-in `argparse`.
    
    `$ gwrap any_cmd_utility.py`

    As long as the script uses `argparse`, gwrap will create a GUI, with check boxes replacing boolean arguments. Drop down menus replacing argument choices. Hovering tooltips for argument help. And store command history for autocompletion.

- Install `dpython` on my coworkers computer, screw up the most usual functions like `range()`, `list()`. Alias python=dpython just for fun.
