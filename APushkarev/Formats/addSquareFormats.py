# Adds square formats

#v1.0.0
#created by: Pushkarev Aleksandr

import nuke

def addSquareFormats():
    for i in range(5):
        res = pow(2, 7+i)
        nuke.addFormat(f'{res} {res} square_{f"{res//1000}K" if res>=1000 else res}')
