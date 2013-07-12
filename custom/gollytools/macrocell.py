'''
macrocell.py
'''
class Node(tuple):
  '''
  Base Node class. Subclasses tuple.
  The first term should always be the index.
  lsl (abstract method -- log side length)
  hsl (half side length)
  sl  (side length)
  i   (index of given Node in macrocell file)
  c   (count live cells)
  c2  (count live virtual cells)
  '''
  def hsl(self):
    '''
    half side length
    '''
    return 1 << (self.lsl()-1)
  def sl(self):
    '''
    side length
    '''
    return 1 << self.lsl()
  def i(self):
    '''
    index of self in macrocell file
    '''
    return self[0]
class Branch(Node):
  '''
  Branch Node (i.e. Any node that is not a leaf).
  Always has length 6
  (index, lsl, child 1, child 2, child 3, child 4)
  '''
  def lsl(self):
    '''
    log side length. Required by abstract superclass Node.
    '''
    return self[1]
  def __repr__(self):
    '''
    Makes the str representation more readable.
    '''
    return 'Branch('+','.join(str(n.i()) for n in self[2:])+')'
class ColorLeaf(Node):
  '''
  Color Leaf.
  Always has length 5
  (index, cell 1, cell 2, cell 3, cell 4)
  '''
  def lsl(self):
    '''
    log side length of Color Leaf is always 1.
    '''
    return 1
  def __repr__(self):
    '''
    Makes str representation more readable
    '''
    return 'Leaf('+','.join(map(str,self[1:]))+')'
class BlackWhiteLeaf(Node):
  '''
  Black White Leaf.
  Always have length 65
  (index, cell 1, ... cell 64)
  '''
  def lsl(self):
    '''
    log side length of Black White Leaf is always 3.
    '''
    return 3
  def __repr__(self):
    '''
    Makes str representation more readable
    '''
    return 'Leaf('+''.join(map(str,self[1:]))+')'
class ZeroLeaf(Node):
  '''
  Zero Leaf.
  Leaf representing all regions with only off nodes
  '''
  def lsl(self):
    '''
    Zero leaf can actually have any dimension.
    However, I will just return 0 here.
    '''
    return 0
  def __getitem__(self,i):
    '''
    ZeroLeaf should actually not have anything in its tuple.
    Just return 0 for any index.
    '''
    return 0
  def __repr__(self):
    '''
    Makes str representable more readable
    '''
    return 'ZeroLeaf()'
class Macrocell(object):
  '''
  Macrocell object.
  nodes -> the list of nodes in order of index.
  update -> callback for when we want to update status
  
  Also, if a bw Macrocell is parsed, nstates is automatically
  set to 2.
  '''
  
  '''
  PART 1
  Methods associated with for constructing Macrocell object,
  and filling it with values
  '''
  def __init__(self):
    '''
    Initialize Macrocell
    '''
    self.nodes = []
    self.update = lambda msg : msg
    self.nstates2 = 0
  def update_to_stream(self,stream):
    self.update = lambda msg : stream.write(msg)
    return self
  def update_to_stdout(self):
    from sys import stdout
    self.update_to_stream(stdout)
    return self
  def from_file(self,file_name):
    with open(file_name,'r')as f:return self.from_string(f.read())
  def from_string(self,s):
    '''
    Assumes s is a str containing the contents of a well formed
    macrocell file.
    '''
    self.nodes = [ ZeroLeaf() ]
    i = 1
    while i<len(s)and not(s[i-1]=='\n'and(s[i]=='1'or s[i]in'.*$')):i+=1
    if i<len(s):
      ptg = 0
      while i < len(s):
        n = [ len(self.nodes) ]
        if s[i] in '*.$':
          j = 1
          while i<len(s) and s[i] in '*.$':
            if   s[i] == '.': n.append(0)
            elif s[i] == '*': n.append(1)
            else:
              j += 8
              while len(n) < j: n.append(0)
            i += 1
          while len(n) < 65: n.append(0)
          self.nodes.append(BlackWhiteLeaf(n))
          while i < len(s) and s[i] != '\n': i += 1
          i += 1
        else:
          j = i+1
          while j < len(s) and s[j] != '\n': j += 1
          ns = list(map(int,s[i:j].split()))
          if ns[0] == 1: self.nodes.append(ColorLeaf(n+ns[1:]))
          else:
            n += [ns[0]] + [self.nodes[ni] for ni in ns[1:]]
            self.nodes.append(Branch(n))
          i = j+1
        if ptg+10 < (100*i)//len(s):
          ptg += 10
          self.update(
            str(ptg)+'% of macrocell data parsed ('+
            str(len(self.nodes))+
            ' nodes)\n')
      self.update(str(len(self.nodes)) +' nodes in macrocell object\n')
    else:
      self.update(
        'no nodes read -- just the 1 zero leaf in macrocell object\n')
    return self
  '''
  PART 2
  Methods associated with assuming each cell represents just itself.
  (constrast with PART 3)
  '''
  def blocks(self,lbsl):
    '''
    lbsl is the logarithm of the block side length.
    
    Iterates over all (non-emtpy) nodes in self of exactly given size.
    Yields triplets (x,y,n) where x, y are the coordinates of the blocks
    (in cells/pixels), and n the node object describing the block.
    
    There is no guarantee as to the order in which they are given.
    '''
    if self.nodes[-1].lsl() < lbsl:
      raise Exception('block size bigger than entire macrocell')
    if self.nodes[1].lsl() > lbsl:
      raise Exception(
        'requested block size smaller than size of smallest block')
    stack = [ (0,0,self.nodes[-1]) ]
    while len(stack) > 0:
      x, y, n = stack.pop()
      if n.i() == 0:
        pass
      elif n.lsl() == lbsl:
        yield x, y, n
      else:
        hs = n.hsl()
        stack.append((x   ,y   ,n[2]))
        stack.append((x+hs,y   ,n[3]))
        stack.append((x   ,y+hs,n[4]))
        stack.append((x+hs,y+hs,n[5]))
  def cells(self):
    '''
    Iterates over all (non-zero colored) cells in self.
    Yields triplets (x,y,c) where x, y are the coordinates of the cell,
    and c is the color of the cell.
    '''
    lsl = self.nodes[1].lsl()
    sl  = self.nodes[1].sl()
    for x,y,n in self.blocks(lsl):
      for dy in range(sl):
        for dx in range(sl):
          c = n[1+dy*sl+dx]
          if c != 0:
            yield x+dx, y+dy, c
  def precount_live_cells(self):
    '''
    calculates densities and returns self
    '''
    for n in self.nodes:
      if isinstance(n,ZeroLeaf):
        n.c = 0
        n.t = 1
        n.c2 = 0
        n.t2 = 2
      elif isinstance(n,Branch):
        n.c = n[2].c + n[3].c + n[4].c + n[5].c
        n.c2 = n[2].c2 + n[3].c2 + n[4].c2 + n[5].c2
        n.t = n[2].t + n[3].t + n[4].t + n[5].t
      elif isinstance(n,BlackWhiteLeaf):
        n.c = 64 - n.count(0)
        n.t = 64
      elif isinstance(n,ColorLeaf):
        n.c = 4  - n.count(0)
        n.t = 4
        n.c2= 8 - [x for xs in n for x in (xs%self.nstates2,xs//self.nstates2)].count(0)
    return self
  def bmp(self,colortable=None):
    '''
    convert self to a bmp object
    '''
    if colortable == None:
      colortable = [(0,0,0),
                    (255,0,0),(0,255,0),(0,0,255),
                    (0,255,255),(255,0,255),(255,255,0),
                    (255,255,255)] + [(255,255,255)] * (256-8)
    from bmp import Bmp8
    sl = self.nodes[-1].sl()
    b = Bmp8(sl,sl,colortable)
    for x,y,c in self.cells(): b[x,y] = c
    return b
  def bmpd(self,lbsl):
    '''
    convert self to a bmp image, based on density
    lbsl is log block side length.
    '''
    from bmp import Bmp8
    bsl = 1 << lbsl
    lsl = self.nodes[-1].lsl() - lbsl
    sl  = 1 << lsl
    b = Bmp8(sl,sl)
    for x,y,n in self.blocks(lbsl):
      b[x//bsl,y//bsl] = (255*n.c)//n.t
    return b
  '''
  PART 3
  Methods associated with assuming each cell represents 2 virtual cells.
  (Like PART 2 but instead twice as wide).
  Unlike in PART 2, in PART 3, it is necessary to know how many states are
  possible in a virtual cell in order to properly figure out which two 
  virtual states are in a physical (golly) state. Therefore, in order
  for these methods to be called, setnstates2 must be called with proper
  argument before these methods may be properly used.
  '''
  def setnstates2(self,nstates2):
    self.nstates2 = nstates2
    return self
  def cells2(self):
    ns = self.nstates2
    for x,y,c in self.cells():
      if c%ns != 0:
        yield 2*x,y,c%ns
      c //= ns
      if c%ns != 0:
        yield 2*x+1,y,c%ns
  def bmp2(self,colortable=None):
    if colortable == None:
      colortable = [(0,0,0),
                    (255,0,0),(0,255,0),(0,0,255),
                    (0,255,255),(255,0,255),(255,255,0),
                    (255,255,255)] + [(255,255,255)] * (256-8)
    from bmp import Bmp8
    sl = self.nodes[-1].sl()
    b = Bmp8(2*sl,sl,colortable)
    for x,y,c in self.cells2(): b[x,y] = c
    return b
  def bmpd2(self,lbsl):
    from bmp import Bmp8
    bsl = 1 << lbsl
    lsl = self.nodes[-1].lsl() - lbsl
    sl  = 1 << lsl
    b = Bmp8(2*sl,sl)
    for x,y,n in self.blocks(lbsl):
      c = n[2].c2 + n[4].c2
      t =(n[2].t  + n[4].t) * 2
      b[x//bsl*2  , y//bsl] = (255*c)//t
      c = n[3].c2 + n[5].c2
      t =(n[3].t  + n[5].t) * 2
      b[x//bsl*2+1, y//bsl] = (255*c)//t
    return b
def debugtest():
  m = Macrocell().setnstates2(3).update_to_stdout().from_file('large.mc').precount_live_cells()
  print(m.nstates2)
  m.bmpd2(4).save('mactest.bmp')
  #m.bmpd(3).save('mactest2.bmp')
  print(len(m.nodes))
  print(m.nodes[:4])