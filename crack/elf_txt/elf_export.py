#!python

import codecs
import struct, sys

def decode_char(n):
  ret = ""
  try:
    ret = codecs.decode(int.to_bytes(n, 1 if (n < 0x80 or (n > 0xa0 and n < 0xe0)) else 2, 'big'), 'sjis')
  except:
    ret = ""
  return ret

def handleBuffer(buf):
  n = 0
  i = 0
  ret = ""
  while i < len(buf):
    n = buf[i]
    if (n >= 0x80 and n <= 0xa0) or n >= 0xe0:
      n = (n << 8) | buf[i+1]
      #n = (n - 0x81) * 128 + buf[i + 1] + 32
      i = i + 2
    elif n == 0:
      break
    else:
      i = i + 1
    dec = decode_char(n)
    if dec == "":
      if n > 0x80:
        dec = "{%X}" % (buf[i - 1] + buf[i - 2] * 0x100)
      else:
        dec = "{%X}" % n
    ret = ret + dec
    n = 0
  return ret

def readAString(fp):
  ret = b''
  while True:
    temp = fp.read(1)
    if temp == b'':
      return ''
    ret = ret + temp
    if temp == b'\x00':
      break
  return ret

# seek point:
# 0x4D87E0
# 0x4D8C08
def main():
  elf_file = open(sys.argv[1], "rb")
  out = open("out.txt", "w")
  while True:
    data = readAString(elf_file)
    if type(data) == str:
      break
    if data == b'' or data == b'\x00':
      continue
    out.write("offset=0x%X\n" % (elf_file.tell() - len(data)))
    out.write("original=%s\n" % handleBuffer(data))
    out.write("target=\n------\n")


if __name__ == "__main__":
  main()
