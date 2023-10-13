import sys, argparse
from widdy.examples import chuck, counter

def main(argv=None):
    demos = {
        'counter': counter.main,
        'chuck':   chuck.main,
    }
    names = list(demos)
    commands = ", ".join(f'`{n}`' for n in names)
    p = argparse.ArgumentParser('widdy', description=f"""
    widdy (C) Uwe Jugel:
    This is the widdy binary to start one or all demos of the widdy Python module.
    Use the `all` command to start all demos consecutively without additional arguments.
    Use one of {commands} to run a single demo, passing any remaining arguments to the demo app.
    """)
    p.add_argument('demo', help='start one or all the demos', choices=names+['all'], default=None)
    args, rest = p.parse_known_args(argv)
    if args.demo == 'all': return [fn() for fn in demos.values()]
    else:                  return demos[args.demo](rest)

if __name__ == '__main__':
    main(sys.argv[1:])
    sys.exit(0)
