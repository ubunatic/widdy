import urwid
from collections import namedtuple
from typing import List
from widdy import styles

import asyncio

MenuItem = namedtuple('MenuItem', 'key style text')
KeyFunc  = namedtuple('KeyFunc',  'key func')

def Pal(*pal_set:List[styles.Style]):
    pal = styles.default_pal.copy()
    pal.update(set(pal_set))
    return list(pal)

def Header(text):
    txt = urwid.Text(text)
    return urwid.AttrMap(txt, styles.INV_BLACK)

def Menu(*items:List[MenuItem], quit=True):
    line = []
    items = list(items)
    if quit: items = items + [('Q', styles.RED_BOLD, 'quit')]
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
        if loop     is None: loop = urwid.AsyncioEventLoop(loop=asyncio.get_event_loop())
        super().__init__(frame, pal, unhandled_input=handlers, event_loop=loop)

