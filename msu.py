import subprocess
import os
import shutil

def expand(source, dest, filter_='*'):
    subprocess.call(['expand', '-F:{}'.format(filter_), source, dest])

