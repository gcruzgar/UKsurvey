"""
author: Gonzalo
date started: 19/10/18
"""

import pandas as pd 

filename1 = "a_indresp.tab"
filename2 = "b_indresp.tab"

df1 = pd.read_csv(filename1, sep='\t')
df2 = pd.read_csv(filename2, sep='\t')

pidp = 1639357682

mstat_1 = df1.loc[df1['pidp'] == pidp, 'a_mlstat'].item() 
mstat_2 = df2.loc[df2['pidp'] == pidp, 'b_mlstat'].item() 

m_evol = [mstat_1, mstat_2]

marital_status = {1: "single, never married/in civil partnership", 2: "married",
    3: "civil partner", 4: "separated from spouse",
    5: "divorced", 6: "widowed",
    7: "separated from civil partner", 8: "former civil partner",
    9: "surviving civil partner", -1: "don't know",
    -9: "missing", -8: "inapplicable",
    -7: "proxy", -2: "refusal"}

print("Individual %d went from %s to %s" % (pidp, marital_status[mstat_1], marital_status[mstat_2]))