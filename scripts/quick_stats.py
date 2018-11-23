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
dim_df.columns = ['Tenure', 'Composition', 'Occupants', 'Rooms', 'Bedrooms']

def plot_dist(dim):

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

for dim in dim_df.columns:
    plot_dist(dim)

dim_metadata = {
    "Tenure": {
        "0": "All categories: Tenure",
        "1": "Owned or shared ownership: Total",
        "2": "Owned: Owned outright",
        "3": "Owned: Owned with a mortgage or loan or shared ownership",
        "4": "Rented or living rent free: Total",
        "5": "Rented: Social rented",
        "6": "Rented: Private rented or living rent free"
    },

    "Composition": {
        "0": "All categories: Household type",
        "1": "One person household",
        "2": "Married or same-sex civil partnership couple household",
        "3": "Cohabiting couple household",
        "4": "Lone parent household",
        "5": "Multi-person household"
    },

    "Occupants": {
        "0": "All categories: Household size",
        "1": "1 person in household",
        "2": "2 people in household",
        "3": "3 people in household",
        "4": "4 or more people in household"
    },

    "Rooms": {
        "0": "All categories: Number of rooms",
        "1": "1 room",
        "2": "2 rooms",
        "3": "3 rooms",
        "4": "4 rooms",
        "5": "5 rooms",
        "6": "6 or more rooms"
    },

    "Bedrooms": {
        "0": "All categories: Number of bedrooms",
        "1": "1 bedroom",
        "2": "2 bedrooms",
        "3": "3 bedrooms",
        "4": "4 or more bedrooms"
    }
}