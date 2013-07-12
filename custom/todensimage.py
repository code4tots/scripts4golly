'''
todensimage.py

Saves the current configuration to a mc, then loads the mc, and converts it to a density image.
'''
import parameters
reload(parameters)
from parameters import mcfn, densbmpfn, nstates, lbsl
from gollytools.macrocell import Macrocell
from gollytools.bmp import display
from golly import save
save(mcfn,'mc')
Macrocell().from_file(mcfn).setnstates2(nstates).precount_live_cells().bmpd(lbsl).save(densbmpfn)
display(densbmpfn)
