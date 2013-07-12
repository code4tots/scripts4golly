'''
rulegen.py

Python tools for creating golly rule files.

Example usage:

name      = "PiggyBack"
rulerange = 2
numstates = 3
def f(a,b,c,d,e):
  x = (b+c+d)%2
  if x == 1:
    return 1
  else:
    l = (a+b+c)%2
    r = (c+d+e)%2
    lcr = [l,c,r]
    lbcdr = [l,b,c,d,r]
    lcr12 = lcr.count(1) + lcr.count(2)
    lbcdr12 = lbcdr.count(1) + lbcdr.count(2)
    if lcr12 == 2 or (lcr12 <= 1 and lbcdr12 in [1,3]):
      return 2
    else:
      return 0
rule = Rule1DV(name,rulerange,numstates,f)
rule.to_golly_rule()

'''
class Rule(object):
  '''
  Abstract base Rule class.
  '''
  def to_file(self):
    '''
    Writes current rule to a file (file name is predetermined by
    self.n).
    '''
    with open(self.n+'.rule','w') as f:
      f.write(str(self))
    return self
  def to_golly_rule(self):
    '''
    Writes the rule file directly into rule directory.
    '''
    from golly import getdir, show
    with open(getdir('rules')+self.n+'.rule','w') as f:
      f.write(str(self))
    show("Saved rule to "+getdir('rules')+self.n+'.rule')
    return self
class Rule1D(Rule):
  '''
  Class for 1-dimensional rules.
  Rule1D only supports 1D rules with range r = 1.
  '''
  def __init__(self,n,s,f):
    '''
    n (rule name)
    s (number of states)
    f (cellular automata function)
    '''
    self.n = n
    self.s = s
    self.f = f
  def table_header(self):
    '''
    Returns a str containing the rule table header.
    '''
    return '\n'.join((
      '@TABLE',
      'n_states:'+str(self.s),
      'neighborhood:Moore',
      'symmetries:none\n'))
  def table_body(self):
    '''
    Returns a str containing the table body.
    '''
    from itertools import product
    s = range(self.s)
    def f(L,C,R):
      ret = self.f(L,C,R)
      if ret in s: return ret
      raise Exception("invalid transtition function")
    def LCRf():
      for L,C,R in product(s,s,s):
        r = f(L,C,R)
        if r != 0:
          yield L,C,R,r
    return '\n'.join(
      ','.join(map(str,[0,C,R,0,0,0,0,0,L,r]))
        for L,C,R,r in LCRf())
  def table(self):
    '''
    Returns a str containing the table
    '''
    return self.table_header() + self.table_body()
  def __str__(self):
    '''
    Returns a str containing the contents of a .rule file
    corresponding to this Rule
    '''
    return '@RULE '+self.n+'\n'+self.table()
class Rule1DV(Rule):
  '''
  Class for 1-dimensional rules.
  Rule1DV (Rule1D virtual). Since golly physically only supports
  range r = 1, we need to encode multiple "virtual" cells into
  single "phsyical" cells.
  '''
  def __init__(self,n,r,s,f):
    '''
    n (rule name)
    r (range -- also the number of virtual cells per physical cell)
    s (number of states each virtual cell can take)
    f (ca function)
    '''
    new_s = s ** r
    if new_s > 255:
      raise Exception("Your rule requires too many states")
    def combine_states(states):
      return sum(state*s**i for i,state in enumerate(states))
    def split_state(state):
      return [(state//(s**i))%s for i in range(r)]
    def new_f(L,C,R):
      L = split_state(L)
      C = split_state(C)
      R = split_state(R)
      return combine_states(f(*(L[i:]+C+R[:i+1]))for i in range(r))
    self.n = n
    self.r = r
    self.s = s
    self.f = f
    self.rule1d = Rule1D(n,new_s,new_f)
  def __str__(self):
    return str(self.rule1d)
def debugtest():
  '''
  For debugging
  '''
  def f(L,C,R):
    return [L,C,R].count(1)%2
  Rule1DV('SampleRule2',1,2,f).to_golly_rule()
  
if __name__ == '__builtin__':
  debugtest()