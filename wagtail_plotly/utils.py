import json
import os
from collections import namedtuple

from django.apps import apps

from .config import PLOTLY_FIGURE_DIRECTORY


def to_float(value):
    try:
        n = float(value)
    except ValueError:
        n = float('NaN')
    return n

def get_layout_dirs():
    paths = []
    for name, ac in apps.app_configs.items():
        path = os.path.join(ac.path, PLOTLY_FIGURE_DIRECTORY)
        if os.path.isdir(path):
            yield path

def get_layout_data(dir):
    for file in os.listdir(dir):
        if not file.endswith(".json"):
            continue
        path = os.path.join(dir, file)
        with open(path) as f:
            yield file, json.load(f)
    
Layout = namedtuple("Layout", "name layout")

def get_layouts():
    layouts = []
    for dir in get_layout_dirs():
        layouts += [Layout(file, layout) for file, layout in get_layout_data(dir)]
    return layouts

LAYOUTS = get_layouts()

def get_member(name, member):
    """
    Retrieves a top level member
    """
    if not name:
        return None

    for layout in LAYOUTS:
        if layout.name == name and member in layout.layout:
            return layout.layout[member]
    return None

def get_layout(name):
    return get_member(name, 'layout')

def get_config(name):
    return get_member(name, 'config')

def get_trace(name):
    return get_member(name, 'trace')

def get_layout_choices():
    choices = [(None, 'Default'),]
    for layout in LAYOUTS:
        choices.append((layout.name, layout.name))
    return choices

