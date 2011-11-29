
import sys
import os


def checkFile(filename):
    if not os.path.exists('share'):
        os.makedirs('share')

    print os.path.isfile('share/' + filename)



checkFile('hold.txt')
checkFile('hold2.txt')

