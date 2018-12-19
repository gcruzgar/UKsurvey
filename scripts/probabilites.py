#!/usr/bin/env python3
import matplotlib.pyplot as plt
import pandas as pd 
import argparse

def transitions(var_name, in_state, var_dict):
    """
    percentage distributions of transitions from in_state in wave w to any state in wave w+1
    """

    #transition_df = pd.DataFrame()
    t_perc_df = pd.DataFrame()
    for wave in range(1,7):
        
        ij_df = pd.concat([var_dict[wave], var_dict[wave+1]], axis=1, join='inner') # inner join between wave w1 and w2

        w1 = chr(96+wave)
        w2 = chr(97+wave)

        is_df = ij_df.loc[ij_df[w1+var_name] == in_state]
        t = is_df[w2+var_name].value_counts()   # frequency of state in w2 given state in_state in w1
        #transition_df[wave] = t

        t_perc = t/sum(t) * 100
        t_perc_df[w1+w2] = t_perc
        
    t_perc_df = t_perc_df.fillna(value=0)
    t_perc_df['average'] = t_perc_df.mean(axis=1)

    t_perc_df.index.name = 'state'
    print("\n%%hh transitions from intial state (%d) in wave w to state in w+1:" % in_state)    
    print(t_perc_df.round(2))

    return t_perc_df

def main ():

    if args.var_name.startswith("_"): # variable to extract
        var_name = args.var_name    
    else:                             # catch variables without underscore
        var_name = '_'+args.var_name
    print("\nvariable: %s" % var_name)

    in_state = args.in_state          # value of initial state
    print("initial state: %d" % in_state)

    n = args.p
    print("Plot %d transitions\n" % n)

    print("Loading household data...\n")
    # household response data - only keep required variables (files are too big to store in memory)
    var_dict = {}
    for wave in range(1,8):

        waveletter = chr(96+wave) # 1 -> "a" etc
        data = pd.read_csv('data/'+waveletter+'_hhresp.tab', sep ='\t')
        var_dict[wave] = data[[waveletter+'_hrpid', waveletter+var_name]].set_index(waveletter+'_hrpid')

    # transitions from wave w to wave w+1
    t_perc_df = transitions(var_name, in_state, var_dict)

    # transitions at any time from given initial state 
    all_waves = pd.concat([var_dict[1], var_dict[2], var_dict[3], var_dict[4], var_dict[5], var_dict[6], var_dict[7]], axis=1, join='inner')
    aw_is = all_waves.loc[all_waves['a'+var_name] == in_state]
    
    # plot transitions
    plt.figure()
    plt.xlabel('Wave')
    plt.ylabel('State')
    plt.title("Household transitions example - %s" % var_name)
    for hh in aw_is.index[0:n]:
        plt.plot(range(1,8), aw_is.loc[hh])
    plt.show()

    # plot average transitions
    av_t = t_perc_df.mean(axis=1)

    plt.figure()
    plt.bar(t_perc_df.index[1:], av_t[1:])
    plt.xlabel('State')
    plt.xticks(t_perc_df.index[1:])
    plt.ylabel('Frequency (%)')
    plt.title("Average probability of transitions between waves - %s" % var_name)
    plt.show()

    c=0
    for i in aw_is.index:
        if (aw_is.loc[i] == in_state).all():
            c+=1 

    print("\nPercentage stable households (present in all waves): %.2f%%" % (c/len(aw_is)*100))
    print("%d/%d households remained at value = %s" % (c, len(aw_is), in_state))

    # transitions from wave a to wave w
    t_aw_df = pd.DataFrame()
    t_aw_perc_df = pd.DataFrame()
    for wave in range(2,8): 

        ij_df = pd.concat([var_dict[1], var_dict[wave]], axis=1, join='inner') # inner join between wave 1 and wave w

        w1 = 'a'
        w2 = chr(96+wave)

        is_df = ij_df.loc[ij_df[w1+var_name] == in_state]
        t = is_df[w2+var_name].value_counts()   # frequency of state in w2 given state in_state in w1
        t_aw_df[wave] = t

        t_perc = t/sum(t) * 100
        t_aw_perc_df[w1+w2] = t_perc

    t_aw_perc_df = t_aw_perc_df.fillna(value=0)
    t_aw_perc_df.index.name = 'state'

    print("\n%%hh transitions from intial state (%d) in wave a to state in w:" % in_state)    
    print(t_aw_perc_df.round(2)) 

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("var_name", type=str, nargs='?', default='_hhtype_dv',
        help="variable of interest to extract. must be in hhresp.tab. type without wave prefix 'w', e.g. _hhtype_dv")   
    parser.add_argument("in_state", type=int, nargs='?', default = 3,
        help="numerical value of initial state")
    parser.add_argument("-p", type=int, nargs='?', default = 3,
        help="number of transitions to plot")     
    args = parser.parse_args()
     
    main()
