'''
toimage2.py

Saves the current configuration to a mc, then loads the mc, and converts it to an image.
Assumes two virtual cells inside every physical (golly) cell.
'''
import parameters
reload(parameters)
from parameters import mcfn, bmpfn2, nstates
from gollytools.macrocell import Macrocell
from gollytools.bmp import display
from golly import save
save(mcfn,'mc')
Macrocell().from_file(mcfn).setnstates2(nstates).bmp2().save(bmpfn2)
display(bmpfn2)
