"""
author: Gonzalo
date started: 19/10/18
"""

import pandas as pd 
from random import randint

filename1 = "a_indresp.tab"
filename2 = "b_indresp.tab"

#pidp = 

def track_event(filename1, filename2, pidp = None):

    df1 = pd.read_csv(filename1, sep='\t')
    df2 = pd.read_csv(filename2, sep='\t')

    while pidp == None:
        r = randint(0, len(df1))
        if r in df2['pidp']:
            pidp = df1['pidp'][r]

    mlstat_1 = df1.loc[df1['pidp'] == pidp, 'a_mlstat'].item() 
    mlstat_2 = df2.loc[df2['pidp'] == pidp, 'b_mlstat'].item() 

    m_evol = [mlstat_1, mlstat_2]

    marital_status = {1: "single, never married/in civil partnership", 2: "married",
        3: "civil partner", 4: "separated from spouse",
        5: "divorced", 6: "widowed",
        7: "separated from civil partner", 8: "former civil partner",
        9: "surviving civil partner", -1: "don't know",
        -9: "missing", -8: "inapplicable",
        -7: "proxy", -2: "refusal"}

    print("Individual %d went from %s to %s" % (pidp, marital_status[mlstat_1], marital_status[mlstat_2]))
    return m_evol

m_evol = track_event(filename1, filename2)
