RED   = '\033[1;31m'  
BLUE  = '\033[1;34m'
CYAN  = '\033[1;36m'
GREEN = '\033[0;32m'
YELLOW = '\033[93m'
RESET = '\033[0;0m'
BOLD    = '\033[;1m'
REVERSE = '\033[;7m'

def color(text, color, reversed=False):
    rv = REVERSE if reversed else ''
    return '%s%s%s%s' % (rv, color, text, RESET)