from widdy import widdy
from random import random
import time, sys

class CounterApp(widdy.App):
    tpl = "{time: <20} | {counter: <7}"

    def __init__(app):
        header      = app.tpl.format(time='time', counter='counter')
        app.headers = [header, len(header) * "-"]
        app.lines   = []
        app.counter = 0
        txt, app.update_text = widdy.Text("")
        box = widdy.LineBox(txt)
        menu     = [('+', widdy.BLUE_BOLD,   'increase'),
                    ('-', widdy.CYAN_BOLD,   'decrease'),
                    ('R', widdy.YELLOW_BOLD, 'random'),
                    ('C', widdy.RED_BOLD,    'clear')]
        handlers = [('+', app.inc),
                    ('-', app.dec),
                    ('R', app.random),
                    ('C', app.clear)]
        f = widdy.Frame(widdy.Header("EmptyApp"), box, widdy.Menu(*menu))
        super().__init__(f, handlers=widdy.Handlers(*handlers))
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
        app.update_text('\n'.join(app.headers + app.lines))

def main(argv=None): CounterApp().run()

if __name__ == '__main__':
    main(sys.argv[1:])
    sys.exit(0)


