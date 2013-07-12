'''
setconf2.py

clears grid and sets just as specified by configuration conf2 in parameters.py
'''
import parameters
reload(parameters)
from parameters import conf2, nstates
from golly import setcell, clear, select, getrect, fit, show
if len(getrect()) > 0:
  select(getrect())
  clear(0)
for i in range(0,len(conf2),2):
  c = conf2[i]
  if i+1 < len(conf2): c += conf2[i+1] * nstates
  setcell(i//2,0,c)
  show(str(i))
select([])
fit()