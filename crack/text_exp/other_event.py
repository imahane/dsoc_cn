#!/bin/python3

import sys
import struct
import codecs

def main():
  fname = sys.argv[1]
  if fname.startswith('ds_event2m') or \
    fname.startswith('ds_eventm'):
      print("这种换另一个去")
      exit(1)

  f = open(fname, 'rb')

  out = open(fname + '.txt', 'w')
  out.write('# 文件名：' + fname + '\n')

  f.seek(0x68)
  textbuf = struct.unpack('<I', f.read(4))[0]
  f.seek(textbuf)
  s = f.read()
  f.seek(textbuf)

  totalbytes = struct.unpack('<I', f.read(4))[0]
  off1 = struct.unpack('<I', f.read(4))[0]
  for i in range(1, 99999999):
    off = struct.unpack('<I', f.read(4))[0]
    loop_end = False
    if off > len(s) or off < off1:
      loop_end = True
      off = len(s)
    length = off - off1 - 1
    off1 += 4
    b = s[off1:off1+length].replace(b'\x82\x40', b'!?').replace(b'\x82\x41', b'!!').rstrip(b'\x00')

    out.write('# ' + str(i) + ' ~~ 0x' + '%X' % off1 + '\n')
    out.write('--------' + '\n')
    try:
      out.write('origin=' + codecs.decode(b, 'shift_jis-2004') + '\n')
    except:
      print(b)
      print(fname)
      exit(1)
    out.write('target=' + '\n\n')
    off1 = off

    if loop_end:
      break


if __name__ == "__main__":
  main()
