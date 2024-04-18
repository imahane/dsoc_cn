#!/usr/bin/env python3

from nlzss.lzss3 import *
import sys

def cmp_splitaaaaa(fname, bts):
  files = bts.split(b'\x00\x00\x00\x00\x10')
  for i in range(0, len(files)):
    b = files[i]
    if i != 0:
      b = b'\x10' + b
    if i != len(files) - 1:
      b = b + b'\x00\x00\x00\x00'
    f2 = open(fname.replace('.cmp', '.raw' + str(i)), 'wb')
    f2.write(b)
    f2.close()

    d = decompress_bytes(b)
    f = open(fname.replace('.cmp', '.dec' + str(i)), 'wb')
    f.write(d)
    f.close()

def cmp_split(fname, bts):
    d = decompress_bytes(bts)
    f = open(fname + '.d', 'wb')
    f.write(d)
    f.close()

def main():
  a = open(sys.argv[1], 'rb')
  b = a.read()
  cmp_split(sys.argv[1], b)
  pass


if __name__ == '__main__':
    exit(main())
