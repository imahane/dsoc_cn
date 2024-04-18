#!/bin/python3

import sys
import struct
import codecs

def main():
  fname = sys.argv[1]
  if not fname.startswith('ds_event2m') and \
    not fname.startswith('ds_eventm'):
      print("文件不符合需求，必须是ds_eventm开头的才能用这个脚本")
      exit(1)

  f = open(fname, 'rb')
  s = f.read()
  f.seek(0)

  out = open(fname + '.txt', 'w')
  out.write('# 文件名：' + fname + '\n')

  total = struct.unpack('<I', f.read(4))[0]
  off1 = struct.unpack('<I', f.read(4))[0]
  for i in range(1, total + 1):
    off = 0
    if i == total + 1:
      off = len(s)
    else:
      off = struct.unpack('<I', f.read(4))[0]
    length = off - off1 - 1
    b = s[off1:off1+length].replace(b'\x82\x40', b'!?').replace(b'\x82\x41', b'!!').rstrip(b'\x00')

    out.write('# ' + str(i) + ' - 0x' + '%X' % off1 + '\n')
    out.write('--------' + '\n')
    try:
      out.write('origin=' + codecs.decode(b, 'shift_jis-2004') + '\n')
    except:
      print(b)
      print(fname)
      exit(1)
    out.write('target=' + '\n\n')
    off1 = off


if __name__ == "__main__":
  main()
