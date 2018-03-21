from ccwid.examples.chuck import Chuck
from ccwid.examples.counter import CounterApp
import time, urwid, io

def run_app(App, timeout=0):
    loop = App()  # type: urwid.MainLoop
    if timeout > 0:
        print("run_app {} start for {:f}s".format(App, timeout))
        loop.start()
        time.sleep(timeout)
        loop.stop()
        print("run_app {} done.".format(App))
    else:
        loop.run()

def main(timeout=0):
    for App in [Chuck, CounterApp]:
        try: run_app(App, timeout)
        except urwid.ExitMainLoop: pass
        except io.UnsupportedOperation: pass

def test_all(): main(timeout=0.5)

if __name__ == '__main__': main(timeout=0)
