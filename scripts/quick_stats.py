#!/usr/bin/env python3
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df = pd.read_csv("data/ssm_hh_E06000047_OA11_2011.csv")
#df.describe()
#df.corr()

# df['LC4408_C_AHTHUK11'].mode()
# df['LC4408_C_AHTHUK11'].unique()
# df['LC4408_C_AHTHUK11'].value_counts()

dim_df = df[['LC4402_C_TENHUK11', 'LC4408_C_AHTHUK11', 'LC4404EW_C_SIZHUK11', 
    'LC4404EW_C_ROOMS', 'LC4405EW_C_BEDROOMS']]


for dim in dim_df.columns:
    
    dim_counts = dim_df[dim].value_counts()
    print("\nfrequency: \n{}".format(dim_counts))
    total = sum(dim_counts)
    dim_counts_perc = dim_counts/total *100
    print("percentage distribution: \n{}".format(dim_counts_perc))

    plt.figure()
    plt.bar(dim_counts.index, dim_counts.values)
    plt.ylabel('Frequency')
    plt.title(dim)
    plt.show() # use block=False to see all 5 plots at the same time 
        # block doesnt work on bash, it will close all graphs.