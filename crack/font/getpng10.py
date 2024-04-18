#!/bin/python

from PIL import Image, ImageDraw, ImageFont
fp = open("Font10x10.cmp.d", "rb")

i = 0
out = Image.new('RGB', (12*16, 217*12))
pic = out.load()
while True:
  buf = fp.read(144)
  if buf == b'':
    break
  x = (i % 16) * 12
  y = (i // 16) * 12
  for a in range(0,12):
    for b in range(0,12):
      c = buf[a * 12 + b]
      pixel = (c, c, c)
      pic[x + b, y + a] = pixel

  i = i + 1

out.save('test3.bmp')
