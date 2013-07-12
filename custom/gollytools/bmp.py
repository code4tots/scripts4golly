'''
bmp.py
Very simple tool for creating bmp files.

Since this is just for gollytools,
I make just really simple tool for creating
24-bit windows BMP files.
'''
def display(image_file_name):
  '''
  opens up the image in the default image viewer.
  '''
  from sys import platform
  from subprocess import call
  if platform.startswith('linux'):
    call(['xdg-open',image_file_name])
  elif platform.startswith('darwin'):
    call(['open',image_file_name])
  elif platform.startswith('win'):
    call(['start', image_file_name], shell=True)
class Bmp(object):
  def __init__(self,filsize,pix_offset,width,height,depth,image_size):
    ba = bytearray(filsize)
    ba[0 ] = 'B'
    ba[1 ] = 'M'
    ba[2 ] = (filsize>>0 )%256
    ba[3 ] = (filsize>>8 )%256
    ba[4 ] = (filsize>>16)%256
    ba[5 ] = (filsize>>24)%256
    ba[10] = (pix_offset>>0 )%256
    ba[11] = (pix_offset>>8 )%256
    ba[12] = (pix_offset>>16)%256
    ba[13] = (pix_offset>>24)%256
    ba[14] = 40
    ba[18] = (width>>0 )%256
    ba[19] = (width>>8 )%256
    ba[20] = (width>>16)%256
    ba[21] = (width>>24)%256
    ba[22] = (height>>0 )%256
    ba[23] = (height>>8 )%256
    ba[24] = (height>>16)%256
    ba[25] = (height>>24)%256
    ba[26] = 1
    ba[28] = (depth>>0 )%256
    ba[29] = (depth>>8 )%256
    ba[34] = (image_size>>0 )%256
    ba[35] = (image_size>>8 )%256
    ba[36] = (image_size>>16)%256
    ba[37] = (image_size>>24)%256
    ba[38] = 19
    ba[39] = 11
    ba[42] = 19
    ba[43] = 11
    self.ba = ba
    self.d = self.depth()
    self.d8 = self.d//8
    self.w = self.width()
    self.h = self.height()
    self.rs = self.rowsize()
    self.off = self.offset()
  def save(self,file_name):
    with open(file_name,'wb') as f:
      f.write(self.ba)
  def depth(self):
    return ((self.ba[28]<<0 )|
            (self.ba[29]<<8 ))
  def width(self):
    return ((self.ba[18]<<0 )|
            (self.ba[19]<<8 )|
            (self.ba[20]<<16)|
            (self.ba[21]<<24))
  def height(self):
    return ((self.ba[22]<<0 )|
            (self.ba[23]<<8 )|
            (self.ba[24]<<16)|
            (self.ba[25]<<24))
  def rowsize(self):
    return (((self.width()*self.depth()+7)//8+3)//4)*4
  def offset(self):
    return ((self.ba[10]<<0 )|
            (self.ba[11]<<8 )|
            (self.ba[12]<<16)|
            (self.ba[13]<<24))
  def pixelpos(self,i):
    x, y = i
    return self.off + self.rs * (self.h-1-y) + self.d8*x
class Bmp24(Bmp):
  '''
  Writes 24-bit bmp files.
  ba -> bytearray of bmp data including header
  '''
  def __init__(self,width,height):
    rowsize = ((width*3+3)//4)*4
    datsize = rowsize * height
    filsize = 54 + datsize
    Bmp.__init__(self,filsize,54,width,height,24,datsize)
  def __setitem__(self,i,v):
    p = self.pixelpos(i)
    r, g, b = v
    self.ba[p+0] = b
    self.ba[p+1] = g
    self.ba[p+2] = r
  def __getitem__(self,i):
    p = self.pixelpos(i)
    b = self.ba[off+0]
    g = self.ba[off+1]
    r = self.ba[off+2]
    return (r,g,b)
class Bmp8(Bmp):
  def __init__(self,width,height,colortable=None):
    if colortable == None:
      colortable = [(i,i,i) for i in range(256)]
    rowsize = (width//4)*4
    image_size = rowsize * height
    pix_offset = 54 + 256 * 4
    filsize = pix_offset + image_size
    Bmp.__init__(self,filsize,pix_offset,width,height,8,image_size)
    for i,(r,g,b) in enumerate(colortable):
      self.ba[54+4*i+0] = b
      self.ba[54+4*i+1] = g
      self.ba[54+4*i+2] = r
  def __getitem__(self,i):
    return self.ba[self.pixelpos(i)]
  def __setitem__(self,i,v):
    self.ba[self.pixelpos(i)] = v
def debugtest():
  width, height = 512, 256
  bmp = Bmp24(width,height)
  for x in range(width):
    for y in range(height):
      bmp[x,y] = ((255*y)//height,255,0)
  bmp.save('sample.bmp')
  
  ct = [(0,0,0),(255,0,0),(0,255,0)] + [(0,0,0)]*(256-3)
  bmp = Bmp8(width,height,ct)
  print(len(bmp.ba))
  print(bmp.width())
  print(bmp.height())
  print(bmp.depth())
  print(bmp.rowsize())
  print(bmp.offset())
  for x in range(width):
    for y in range(height):
      bmp[x,y] = 2
  
  bmp.save('sample8.bmp')