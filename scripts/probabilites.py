#!/usr/bin/env python3
import matplotlib.pyplot as plt
import pandas as pd 
import argparse
from common import transitions
import seaborn as sns

def main ():

    if args.var_name.startswith("_"): # variable to extract
        var_name = args.var_name    
    else:                             # catch variables without underscore
        var_name = '_'+args.var_name
    print("\nvariable: %s" % var_name)

    in_state = args.in_state          # value of initial state
    print("initial state: %d" % in_state)

    print("Loading household data...\n")
    # household response data - only keep required variables (files are too big to store in memory)
    var_dict = {}
    for wave in range(1,8):

        waveletter = chr(96+wave) # 1 -> "a" etc
        data = pd.read_csv('data/'+waveletter+'_hhresp.tab', sep ='\t')                
        data = data.loc[data[waveletter+var_name]>=0] # Drop any missing values
        var_dict[wave] = data[[waveletter+'_hrpid', waveletter+var_name]].set_index(waveletter+'_hrpid')

    # transitions from wave w to wave w+1
    t_perc_df = transitions(var_name, in_state, var_dict)[0]
    t_perc_df.index.name = 'final state'
    print("\n%%hh transitions from intial state (%d) in wave w to state in w+1:" % in_state)    
    print(t_perc_df.round(2))

    # transitions at any time from given initial state 
    all_waves = pd.concat([var_dict[1], var_dict[2], var_dict[3], var_dict[4], var_dict[5], var_dict[6], var_dict[7]], axis=1, join='inner')
    aw_is = all_waves.loc[all_waves['a'+var_name] == in_state]

    # plot average transitions
    av_t = t_perc_df['average'].drop(in_state)

    plt.figure()
    plt.bar(av_t.index, av_t)
    plt.xlabel('State')
    plt.xticks(av_t.index)
    plt.ylabel('Frequency (%)')
    plt.title("Average probability of transitions between waves \n%s - initial state = %d" % (var_name[1:], in_state))
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
        t = is_df.groupby(w2+var_name)[w2+var_name].count() # frequency of state in w2 given state in_state in w1
        t_aw_df[wave] = t

        t_perc = t/sum(t) * 100
        t_aw_perc_df[w1+w2] = t_perc

    t_aw_perc_df = t_aw_perc_df.fillna(value=0)
    t_aw_perc_df.index.name = 'final state'

    print("\n%%hh transitions from intial state (%d) in wave a to state in w:" % in_state)    
    print(t_aw_perc_df.round(2)) 

    # plot probabilities
    ax = sns.heatmap(t_aw_perc_df.drop(in_state).round(2), annot=True, linewidth=.5, cmap="GnBu", cbar_kws={'label':'Percentage (%)'})
    ax.set_xlabel('wave')
    ax.set_title('Transitions probabilities  - %s \ninitial state = %d' % (var_name[1:], in_state))
    plt.show()

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("var_name", type=str, nargs='?', default='_hhtype_dv',
        help="variable of interest to extract. must be in hhresp.tab. type without wave prefix 'w', e.g. _hhtype_dv")   
    parser.add_argument("in_state", type=int, nargs='?', default = 3,
        help="numerical value of initial state")    
    args = parser.parse_args()
     
    main()
