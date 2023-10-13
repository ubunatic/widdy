#!/usr/bin/env python
import widdy
from widdy.examples.chuck import Chuck
from widdy.examples.counter import CounterApp
import time, urwid, io

def run_app(app:widdy.App, timeout=0):
    loop = app()
    if timeout > 0:
        print("run_app {} start for {:f}s".format(app, timeout))
        loop.start()
        time.sleep(timeout)
        loop.stop()
        print("run_app {} done.".format(app))
    else:
        loop.run()

def main(timeout=0):
    for App in [Chuck, CounterApp]:
        try: run_app(App, timeout)
        except urwid.ExitMainLoop: pass
        except io.UnsupportedOperation: pass

def test_all(): main(timeout=0.5)

if __name__ == '__main__': main(timeout=0)
