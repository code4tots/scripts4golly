'''
parameters_template.py

You modify the values here, then run other scripts to do things,
for instance, run "create_rule.py" to create a correspnding rule file and
save it to golly's rule directory.

parameters_template.py is just a file that could be a template for
parameters.py
'''

'''
configuration
'''
conf = [2, 1, 1, 1]
conf2 = [1,1,1,1,1]
conf2 = [1,0,0,0,1,1,0,1,1]

'''
log block side length, of block for density grouping
'''
lbsl = 3

'''
How many states are possible for a (virtual) cell?
num_states only for situations where there are more than one virtual cell for
every physical cell.
'''
nstates = 3

'''
For saving current configuration (as macrocell)
'''
mcfn  = 'current.mc'

'''
For saving current configuraiton to image
'''
bmpfn  = 'current.bmp'
bmpfn2 = 'current2.bmp'
densbmpfn = 'currentdens.bmp'
densbmpfn2 = 'currentdens2.bmp'

'''
For rule generation
'''
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