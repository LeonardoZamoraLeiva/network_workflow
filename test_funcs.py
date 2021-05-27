#from bigscape_script import bigscape_func, modify_output
from antismash import antismash_func, for_bigscape
import os

antismash_func()
for file in os.listdir('antismash'):
    for_bigscape(file)
