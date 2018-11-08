# UKsurvey

The objective of this project is to visualise the transitions that occur in the microsynthesis of population.  
Understanding Society data is used to complement ONS census data.

For now, the repository is a list of scripts I am using for analysis.

Things to do:
- update Readme
- could use ukcensusapi module to obtain census data
- create python module 


### Understanding Society Dataset

Data can be downloaded from UK Data Service: https://beta.ukdataservice.ac.uk/datacatalogue/series/series?id=2000053
    Requires registration in the UK Data Service website. 
    
Downloading the survey yields two folders: mrdoc and tab, the former contains documentation (including data dictionaries) and the latter the survey response data.

Data is divided into years or waves, each saved in its own subfolder.
The survey changes over time so each folder will contain a different amount of files.
However, there is a set of common files:

- **_w_callrec.tab_**
- **_w_child.tab_**
- **_w_ego_alt.tab_**
- **_w_hhresp.tab_**
- **_w_hhsamp.tab_**
- **_w_income.tab_**
- **_w_indall.tab_**
- **_w_indresp.tab_**
- **_w_youth.tab_**

Where w_ is a prefix denoting the wave (a_, b_, c_ ...)


More information on the survey can be found here: https://www.understandingsociety.ac.uk
