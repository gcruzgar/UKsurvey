"""
Common functions used in scripts
"""
import pandas as pd

def remap(table, column, mapping):
    """ Remaps to values in mapping and discards unmapped values """
    # first remove any values that are not keys in the mapping
    table = table[table[column].isin(mapping.keys())]
    # now map the values
    table[column].replace(mapping, inplace=True)
    return table

def constrain(table, column, minval, maxval, shift=0):
    """ Constrains values like so:
        - removes rows with values < minval
        - caps column values at maxval
        - shift values by shift (e.g. to allow for 0 to mean 1 bedroom)
    """
    table = table[table[column] >= minval]
    table.loc[table[column] > maxval, column] = maxval
    table[column] = table[column] + shift
    return table

def longevity(filelist):
    """ List of individuals that are present in all waves """
    pidp_dic = {}
    wc=1
    for name in filelist:
        print("Loading wave %d data..." % wc)
        df = pd.read_csv(name, sep='\t')
        pidp_dic[str(wc)] = df['pidp']
        wc+=1
    
    id_int = set(pidp_dic['2']).intersection(set(pidp_dic['1']))
    for n in range(3,len(filelist)+1):
        id_int = set(pidp_dic[str(n)]).intersection(id_int)
    return id_int

def hh_list():
    """
    Generate a dataframe with the w_hidp corresponding to each pidp, 
    as well as the sex and year of birth for filtering purposes.
    """
    print("Generating household list...")
    data = pd.read_csv('data/xwaveid.tab', sep ='\t')
    data = data.loc[data['fwintvd_dv'] != -21.0]  # drop any entries with no data from UKHLS. 

    # only save households ids and variables needed for filtering
    hidp_list = data[['pidp', 'sex', 'birthy', 'a_hidp', 'b_hidp', 'c_hidp', 'd_hidp', 'e_hidp', 'f_hidp', 'g_hidp']]
  
    # only need one row per household. Drop duplicates caused by multiple members sharing a household.
    hidp_list = hidp_list.drop_duplicates(subset=['a_hidp', 'b_hidp', 'c_hidp', 'd_hidp', 'e_hidp', 'f_hidp', 'g_hidp'])

    #hidp_list.to_csv('data/xwave_hh_list.csv', index=False)

    return hidp_list

def track_hh(pidp, waves, var_name, hidp_list, var_dict):
    """ 
    Track households over time. Read the hidps for a hh and extract their corresponding values of hh_var.
    Outputs the values for the chosen variable for any given number of waves. 
    """

    hh_row = hidp_list.loc[hidp_list['pidp'] == pidp] # household the individual is a member off in each wave 
    
    track_vals = []
    for wave in waves:
        waveletter = chr(96+wave) # 1 -> "a" etc    

        hh_var = var_dict[wave]
           
        w_val = hh_var.loc[hh_var[waveletter+'_hidp'] == hh_row[waveletter+'_hidp'].item(), waveletter+var_name].values #extract value for the hh at that wave
        if w_val.size == 0: #if the household wasn't present in a wave, set it's value to '-9'
            w_val = [-9]
        track_vals.extend(w_val)  
    
    return track_vals

def transitions(var_name, in_state, var_dict):
    """
    percentage distributions of transitions from in_state in wave w to any state in wave w+1
    """

    t_df = pd.DataFrame()
    for wave in range(1,7):
        
        ij_df = pd.concat([var_dict[wave], var_dict[wave+1]], axis=1, join='inner') # inner join between wave w1 and w2

        w1 = chr(96+wave)
        w2 = chr(97+wave)

        is_df = ij_df.loc[ij_df[w1+var_name] == in_state]   # frequency of state in w2 given state in_state in w1
        t = is_df.groupby(w2+var_name)[w2+var_name].count()

        t_df = pd.concat([t_df, t], axis=1)

    t_df = t_df.dropna(axis=1, how='all') # drop empty columns
    t_df = t_df.fillna(value=0)           # fill remaining missing values wiht zeros  

    t_perc_df = (t_df / t_df.sum()) *100

    # row average
    t_ave = t_perc_df.mean(axis=1)
    t_perc_df['average'] = t_ave

    return t_df, t_ave
