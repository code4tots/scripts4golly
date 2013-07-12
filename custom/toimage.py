'''
toimage.py

Saves the current configuration to a mc, then loads the mc, and converts it to an image.
'''
import parameters
reload(parameters)
from parameters import mcfn, bmpfn
from gollytools.macrocell import Macrocell
from gollytools.bmp import display
from golly import save
save(mcfn,'mc')
Macrocell().from_file(mcfn).bmp().save(bmpfn)
display(bmpfn)
