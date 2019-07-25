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


`$ dpython config inspect-script`


<!--
![start_end_app](https://raw.githubusercontent.com/Madoshakalaka/gapp/master/readme_assets/start_end_app.PNG)
-->

<!--You picture won't show on pypi if you use relative path.-->
<!--If you want to add any image, please add the image to readme_assets folder and add the filename as below-->
<!--![some show case picture](https://raw.githubusercontent.com/Madoshakalaka/gapp/master/readme_assets/showcasePicture.png)-->
