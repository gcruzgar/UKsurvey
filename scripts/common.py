"""
Common functions used in scripts
"""

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