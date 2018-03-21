import asyncio
import urwid, json, requests
import urwid.canvas
from typing import Callable, Tuple, List

default_pal = {
    'inv-black':  ('black',           'white'),
    'green-bold': ('dark green,bold', ''),
    'red-bold':   ('dark red,bold',   ''),
    'blue-bold':  ('dark blue,bold',  ''),
    'green':      ('dark green',      ''),
    'red':        ('light red',       ''),
    'blue':       ('dark blue',       ''),
}

INV_BLACK  = 'inv-black'
RED_BOLD   = 'red-bold'
GREEN_BOLD = 'green-bold'
BLUE_BOLD  = 'blue-bold'
BLUE       = 'blue'
GREEN      = 'green'
RED        = 'red'
YELLOW     = 'yellow'
CYAN       = 'cyan'

def Pal(pal_dict=None):
    pal = default_pal.copy()
    if pal_dict is not None: pal.update(pal_dict)
    return [(k,) + tuple(t) for k, t in pal.items()]

def Header(text):
    txt = urwid.Text(text)
    return urwid.AttrMap(txt, INV_BLACK)

def Menu(*options:List[tuple], quit=True):
    line = []
    options = list(options)
    if quit: options = options + [('Q', RED_BOLD, 'quit')]
    for key, style, info in options:
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

def Handlers(*key_funcs:List[tuple], quit=True):
    def handle(key):
        if quit and key in ('Q', 'q'): raise urwid.ExitMainLoop()
        for k, fn in key_funcs:
            if key in (k.lower(), k.upper()): fn()
    return handle

class App(urwid.MainLoop):
    def __init__(app, frame, handlers=None, pal=None, loop=None):
        if pal      is None: pal      = Pal()
        if handlers is None: handlers = Handlers()
        if loop     is None: loop     = urwid.AsyncioEventLoop(loop=asyncio.get_event_loop())
        super().__init__(frame, pal, unhandled_input=handlers, event_loop=loop)

