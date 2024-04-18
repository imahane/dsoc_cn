#!/bin/python

from PIL import Image, ImageDraw, ImageFont
fp = open("Font13x13.cmp.d", "rb")

i = 0
out = Image.new('RGB', (240, 3255))
pic = out.load()
while True:
  buf = fp.read(225)
  if buf == b'':
    break
  x = (i % 16) * 15
  y = (i // 16) * 15
  for a in range(0,15):
    for b in range(0,15):
      c = buf[a * 15 + b]
      pixel = (c, c, c)
      pic[x + b, y + a] = pixel

  i = i + 1

out.save('test2.bmp')
