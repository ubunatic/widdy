import sys, urwid, json, requests
import urwid.canvas
from collections import namedtuple
from typing import Callable, Tuple, List, Set

MenuItem = namedtuple('MenuItem', 'key style text')
KeyFunc  = namedtuple('KeyFunc',  'key func')
Style    = namedtuple('Style',    'name fg bg')

default_pal = {
    Style('inv-black',    'black',             'light gray'),

    Style('green-bold',   'dark green,bold',   ''),
    Style('red-bold',     'dark red,bold',     ''),
    Style('blue-bold',    'dark blue,bold',    ''),
    Style('yellow-bold',  'yellow,bold',       ''),
    Style('magenta-bold', 'dark magenta,bold', ''),
    Style('cyan-bold',    'dark cyan,bold',    ''),

    Style('green',        'dark green',        ''),
    Style('red',          'dark red',          ''),
    Style('blue',         'dark blue',         ''),
    Style('cyan',         'dark cyan',         ''),
    Style('magenta',      'dark magenta',      ''),
    Style('yellow',       'yellow',            ''),
}

INV_BLACK    = 'inv-black'

RED_BOLD     = 'red-bold'
GREEN_BOLD   = 'green-bold'
BLUE_BOLD    = 'blue-bold'
MAGENTA_BOLD = 'magenta-bold'
CYAN_BOLD    = 'cyan-bold'
YELLOW_BOLD  = 'yellow-bold'

BLUE         = 'blue'
GREEN        = 'green'
RED          = 'red'
MAGENTA      = 'magenta'
CYAN         = 'cyan'
YELLOW       = 'yellow'

def Pal(*pal_set:List[Style]):
    pal = default_pal.copy()
    pal.update(set(pal_set))
    return list(pal)

def Header(text):
    txt = urwid.Text(text)
    return urwid.AttrMap(txt, INV_BLACK)

def Menu(*items:List[MenuItem], quit=True):
    line = []
    items = list(items)
    if quit: items = items + [('Q', RED_BOLD, 'quit')]
    for key, style, info in items:
        line.extend(['[', (style, key), ' ', info, '] '])
    return urwid.Text(line)

def Text(alt="", **uw_args):
    txt = urwid.Text(alt, **uw_args)
    def update(text): txt.set_text(text)
    return txt, update

def LineBox(w, bottom=0, top=0, left=0, right=0, valign='top'):
    fil = urwid.Filler(w, top=top, bottom=bottom, valign=valign)
    pad = urwid.Padding(fil, left=left, right=right)
    return urwid.LineBox(pad)

def Frame(header, body, footer):
    return urwid.Frame(header=header, body=body, footer=footer)

def Handlers(*key_funcs:List[KeyFunc], quit=True):
    def handle(key):
        if quit and key in ('Q', 'q'): raise urwid.ExitMainLoop()
        for k, fn in key_funcs:
            if key in (k.lower(), k.upper()): fn()
    return handle

class App(urwid.MainLoop):
    def __init__(app, frame, handlers=None, pal=None, loop=None):
        if pal      is None: pal      = Pal()
        if handlers is None: handlers = Handlers()
        super().__init__(frame, pal, unhandled_input=handlers, event_loop=loop)

