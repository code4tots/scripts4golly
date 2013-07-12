'''
create_rule.py

A convenient python script you can run from inside golly to create a new 1-D 
rule for golly using the information in rule.py.

calling the method "rule.to_golly_rule()" requires the golly module, which is
only available if this script is called from inside golly.

If to_golly_rule fails, I try to call to_file instead, to save the file to the
current directory.
'''
import parameters
reload(parameters)
from parameters import name, rulerange, numstates, f
from gollytools.rulegen import Rule1DV
rule = Rule1DV(name,rulerange,numstates,f)
try:rule.to_golly_rule()
except:rule.to_file()