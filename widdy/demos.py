import sys, argparse
from widdy.examples import chuck, counter

def main(argv=None):
    demos = {
        'counter': counter.main,
        'chuck':   chuck.main,
    }
    names = list(demos)
    p = argparse.ArgumentParser('widdy', description="""
    widdy (C) Uwe Jugel:
    This is the widdy binary to start one or all demos of the widdy python3 module.
    Use the `all` command to start all demos consecutively without additional arguments.
    Use one of `{names}` to run a single demo, passing any remaining arguments to the demo app.
    """.format(names='`, `'.join(names)))
    p.add_argument('demo', help='start one or all the demos', choices=names+['all'], default=None)
    args, rest = p.parse_known_args(argv)
    if args.demo == 'all': return [fn() for fn in demos.values()]
    else:                  return demos[args.demo](rest)

if __name__ == '__main__':
    main(sys.argv[1:])
    sys.exit(0)
