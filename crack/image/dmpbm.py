from PIL import Image, ImageDraw

class DMPBM:
  tiled3ds = [
    0,  1,  8,  9,  2,  3, 10, 11,
    16, 17, 24, 25, 18, 19, 26, 27,
    4,  5, 12, 13,  6,  7, 14, 15,
    20, 21, 28, 29, 22, 23, 30, 31,
    32, 33, 40, 41, 34, 35, 42, 43,
    48, 49, 56, 57, 50, 51, 58, 59,
    36, 37, 44, 45, 38, 39, 46, 47,
    52, 53, 60, 61, 54, 55, 62, 63
  ]
  def __init__(self, fname):
    f = open(fname, 'rb')
    self.fname = fname
    self.magic = f.read(5)
    self.pattern = f.read(1)[0]
    self.width = int.from_bytes(f.read(4), 'little')
    self.height = int.from_bytes(f.read(4), 'little')

    if self.pattern == 0x01:  # RGBA5551
      self.pixeldata = f.read(self.width * self.height * 2)
    elif self.pattern == 0x02:  # RGBA4444
      self.pixeldata = f.read(self.width * self.height * 2)
    elif self.pattern == 0x03:  # RGBA8888
      self.pixeldata = f.read(self.width * self.height * 4)
    elif self.pattern == 0x00:  # Alpha8
      self.pixeldata = f.read(self.width * self.height * 1)
    else:
      print(fname + ": not written pattern %X" % self.pattern)
      exit(1)
    f.close()

  def toPNG(self):
    img = Image.new('RGBA', (self.width, self.height))
    pic = img.load()
    current = 0
    while current < len(self.pixeldata):
      pixel_idx = 0
      pixel_data = None
      if self.pattern == 0x01:  # RGBA5551
        tmp = self.pixeldata[current:current + 2]
        tmp = int.from_bytes(tmp, 'little')
        pixel_data = (
          (tmp & 0xF800) >> 8,
          (tmp & 0x7C0) >> 3,
          (tmp & 0x3E) << 2,
          (tmp & 0x1) * 255)
        pixel_idx = current // 2
        current = current + 2
      elif self.pattern == 0x02:  # RGBA4444
        tmp = self.pixeldata[current:current + 2]
        tmp = int.from_bytes(tmp, 'little')
        pixel_data = ((tmp >> 12) << 4, ((tmp >> 8) & 0xF) << 4, ((tmp >> 4) & 0xF) << 4, (tmp & 0xF) << 4)
        pixel_idx = current // 2
        current = current + 2
      elif self.pattern == 0x03:  # RGBA8888
        tmp = self.pixeldata[current:current + 4]
        tmp = int.from_bytes(tmp, 'little')
        pixel_data = (tmp >> 24, (tmp >> 16) & 0xFF, (tmp >> 8) & 0xFF, tmp & 0xFF)
        pixel_idx = current // 4
        current = current + 4
      elif self.pattern == 0x00:  # alpha8
        tmp = self.pixeldata[current:current + 1]
        tmp = int.from_bytes(tmp, 'little')
        pixel_data = (255, 255, 255, tmp)
        pixel_idx = current // 1
        current = current + 1
      else:
        print("not written pattern %X" % self.pattern)
        exit(1)

      x0 = (pixel_idx // 64) % (self.width / 8) * 8
      y0 = (pixel_idx // 64) // (self.width / 8) * 8
      pixel_idx = self.tiled3ds[pixel_idx % 64]
      x = (pixel_idx % 64) % 8
      y = (pixel_idx % 64) // 8
      pic[x0 + x, y0 + y] = pixel_data

    img = img.transpose(Image.FLIP_TOP_BOTTOM)
    img.save(self.fname + ".png")
    img.close()
