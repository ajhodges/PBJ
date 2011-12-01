# activate virtualenv
import os
activate_this = os.path.expanduser("env/bin/activate_this.py")
execfile(activate_this, dict(__file__=activate_this))

import sys
import os


def checkFile(filename):
    if not os.path.exists('share'):
        os.makedirs('share')

    print os.path.isfile('share/' + filename)



checkFile('hold.txt')
checkFile('hold2.txt')

