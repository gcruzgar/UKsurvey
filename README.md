# UKsurvey

The objective of this project is to visualise the transitions that occur in the microsynthesis of population.  
Understanding Society data is used to complement ONS census data.

Data can be downloaded from UK Data Service: https://beta.ukdataservice.ac.uk/datacatalogue/series/series?id=2000053
    Requires registration in the UK Data Service website. 

More information on the survey can be found here: https://www.understandingsociety.ac.uk

For now, the repository is a list of scripts I am using for analysis.

Things to do:
- update Readme
- could use ukcensusapi module to obtain census data
- create python module 


### Understanding Society Dataset

Downloading the survey yields two folders: mrdoc and tab, the former contains documentation (including data dictionaries) and the latter the survey response data.

Data is divided into years or waves, each saved in its own subfolder.
The survey changes over time so each folder will contain a different amount of files.
However, there is a set of common files. These share filename except for a prefix denoting the wave (w_):
