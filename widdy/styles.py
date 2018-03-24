from collections import namedtuple

Style = namedtuple('Style', 'name fg bg')

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
