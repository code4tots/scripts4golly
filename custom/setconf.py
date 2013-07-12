'''
setconf.py

clears grid and sets just as specified by configuration conf in parameters.py
'''
import parameters
reload(parameters)
from parameters import conf
from golly import setcell, clear, select, getrect, fit
if len(getrect()) > 0:
  select(getrect())
  clear(0)
for i, s in enumerate(conf): setcell(i,0,s)
select([])
fit()