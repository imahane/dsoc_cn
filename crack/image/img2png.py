#!/bin/python3

import sys
from dmpbm import *

def main():
  fname = sys.argv[1]
  f = open(fname, 'rb')
  magic = f.read(5)
  f.seek(0)

  if magic != b'DMPBM':
    print('not a dmpbm img: ' + fname)
    exit(1)

  d = DMPBM(fname)
  d.toPNG()

if __name__ == '__main__':
  main()


