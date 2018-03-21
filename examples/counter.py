from ccwid import ccwid
from random import random
import time

class CounterApp(ccwid.App):
    tpl = "{time: <20} | {counter: <7}"

    def __init__(app):
        header      = app.tpl.format(time='time', counter='counter')
        app.headers = [header, len(header) * "-"]
        app.lines   = []
        app.counter = 0
        txt, app._update_text = ccwid.Text("")
        box = ccwid.LineBox(txt)
        menu     = [('+', ccwid.BLUE_BOLD, 'increase'),
                    ('-', ccwid.BLUE_BOLD, 'decrease'),
                    ('R', ccwid.YELLOW,    'random'),
                    ('C', ccwid.RED_BOLD,  'clear')]
        handlers = [('+', app.inc),
                    ('-', app.dec),
                    ('R', app.random),
                    ('C', app.clear)]
        f = ccwid.Frame(ccwid.Header("EmptyApp"), box, ccwid.Menu(*menu))
        super().__init__(f, handlers=ccwid.Handlers(*handlers))
        app.redraw()

    def inc(app):    app.counter += 1; app.add_value()
    def dec(app):    app.counter -= 1; app.add_value()
    def random(app): app.counter = int(100 * random()); app.add_value()
    def clear(app):  app.lines = []; app.redraw()

    def add_value(app, value=None):
        if value is None: value = app.counter
        app.lines.append(app.tpl.format(time='{:.2f}'.format(time.time()), counter=value))
        app.redraw()

    def redraw(app):
        app._update_text('\n'.join(app.headers + app.lines))

def main(): CounterApp().run()

if __name__ == '__main__': main()

