''' PBJ
    Camden Clements
    Adam Hodges
    Zach Welch
    
    lookup.py is a proof of concept for searching the share directory
'''

# activate virtualenv
import os
activate_this = os.path.expanduser("env/bin/activate_this.py")
execfile(activate_this, dict(__file__=activate_this))

import sys
import os

from pbj import SHARE_PATH

def checkFile(filename):
    if not os.path.exists(SHARE_PATH):
        os.makedirs(SHARE_PATH)

    print os.path.isfile(SHARE_PATH + '/' + filename)



checkFile('hold.txt')
checkFile('hold2.txt')

