"""Auto importing controllers"""
import importlib
import os

# get the current directory and
current_dir = os.path.dirname(os.path.realpath(__file__))

# get all .py files in the directory
index_files = [
    f[:-3] for f in os.listdir(current_dir) if f.endswith(".py") and f != "__init__.py"
]
api_files = [
    f[:-3]
    for f in os.listdir(os.path.join(current_dir, "api"))
    if f.endswith(".py") and f != "__init__.py"
]

# import each module and add its variables to the blueprints variable
blueprints = []


def add_module(module_data, name):
    attr_value = getattr(module_data, name)
    if (
        not isinstance(attr_value, type)
        and not name.startswith("__")
        and (name.endswith("routing") or name.endswith("blueprint"))
    ):
        blueprints.append(attr_value)
        globals()[name] = attr_value


for file in index_files:
    module = importlib.import_module("." + file, package=__name__)
    for attr_name in dir(module):
        add_module(module, attr_name)

for file in api_files:
    module = importlib.import_module(".api." + file, package=__name__)
    for attr_name in dir(module):
        add_module(module, attr_name)
