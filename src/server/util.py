## file: util.py is a set of functions for the system

import re

def checkEmail(email):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return False
    else:
        return True
    