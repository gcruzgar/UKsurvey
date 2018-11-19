# UKsurvey

Things to do:
- keep Readme updated
- could use ukcensusapi module to obtain census data
- give examples for every script?
- create python module 

## Table of contents
1. [Introduction](#introduction)    
    1.1. [SPENSER](#spenser)
2. [Data](#data)    
    2.1.[Understanding Society](#understanding-society)    
    2.2.[Census](#census)    
    2.3.[Comparing Survey and Census Data](#comparing-survey-and-census-data)
3. [Household Microsynthesis](#household-microsynthesis)
4. [Method](#method)    
    4.1.[Mapping Survey to Census](#mapping-survey-to-census)

## Introduction
The objective of this project is to visualise the transitions that occur in the microsynthesis of population. This is part of a bigger project aiming to create a framework for customisable population estimates (see SPENSER). Here, understanding Society data is used to complement ONS census data. In the future, other datasets will be added. (consumer data, information on migration etc.)

For now, the repository is a list of scripts I am using for analysis.

### SPENSER 
Synthetic Population Estimation and Scenario Projection Model (SPENSER) is a synthetic population estimation and projection model which uses dynamic microsimulation. It provides the framework for estimates of population which are dynamic and high resolution (at household level); and a comprehensive set of tools for user customisable scenario projections. This project is in development by the University of Leeds.

## Data
### Understanding Society

Longitudinal study of the behaviour of ~40,000 households across the UK.

Data can be downloaded from [UK Data Service](https://beta.ukdataservice.ac.uk/datacatalogue/series/series?id=2000053).
    
Downloading the survey yields two folders: mrdoc and tab, the former contains documentation (including data dictionaries) and the latter the survey response data.

Data is divided into years or waves, each saved in its own subfolder.
The survey changes over time so each folder will contain a different amount of files.
However, there is a set of common files:

- **_w_callrec.tab_**
- **_w_child.tab_**
- **_w_egoalt.tab_**
- **_w_hhresp.tab_**
- **_w_hhsamp.tab_**
- **_w_income.tab_**
- **_w_indall.tab_**
- **_w_indresp.tab_**
- **_w_youth.tab_**

Where w_ is a prefix denoting the wave. The first wave is denoted a, second wave is b etc.    
Individuals have a unique ID (*pidp*), which is persistent throughout the study. Households also have their own ID (*w_hidp*), nonetheless this is wave specific, thus cannot be used to link information across waves. This means an individual's evolution can be tracked over time, but household transitions have an added layer of complexity. 

The largest files are the individual survey responses (**_w_indresp.tab_**). The other group of files of interest are the household response files (**_w_hhresp.tab_**).

|File name |Number of variables* |Description                                          |
|----------|---------------------|-----------------------------------------------------|
|w_hhresp  |200-550              | Substantive data from responding households          
|w_indresp |1300-2900            | Substantive data from responding adults (16+)        
|w_youth   |120-170              | Substantive data from youth questionnaire (10-15)    
|w_hhsamp  |50-200               | Data from Address Record File for issued households  
|w_indall  |100-200              | Household grid data for all persons in household, including children and non respondents
|w_child   |130-350              | Childcare, consents and school information of all children in the household 
|w_egoalt  |10-25                | Kin and other relationships between pairs of individuals in the household

<sub><nowiki>*<nowiki>Questions asked in the survey changed every year, so the number of variables is inconsistent.<sub>

There is another subfolder with cross wave data. It consists of three files:

|File name |Description                                           |
|----------|------------------------------------------------------|
|xwavedat  | Substantive data from responding households          |
|xivdata   | Substantive data from responding adults (16+)        |
|xwaveid   | Individual and household identifiers across all waves|

Cross wave files contain data from every wave, however, the files are small compared to __indresp__ and don't seem to have anything useful for microsynthesis - other than the identifiers in __xwaveid__.

There is considerable attrition in this survey, this is partially compensated by introducing new households in each wave, however, there is a net 23% decrease in housholds over the first 7 years.

More information on the survey can be found here: https://www.understandingsociety.ac.uk.

### Census

The Office for National Statistics produces a national population census every 10 years.    
ONS gives free access to the latest one - currently 2011. The census is the most accurate representation of population data available, thus is often used for population microsynthesis. However, it only occurs once every 10 years and lacks behavioural and consumer data. This is why it is important to complement census with other datasets.   

Data can be obtained directly from [Nomisweb](https://www.nomisweb.co.uk).    
See [UKCensusAPI](https://github.com/virgesmith/UKCensusAPI) for a `python` and `R` wrapper.

### Comparing Survey and Census Data


## Household Microsynthesis

Possible changes to a household:
- Ageing
- Marriage / civil partnership
- Birth of a child / adoption
- Divorce / separation
- Death of a member
- Child moving out due to higher education / employment
- Member returning from higher study
- Changes in employment / retirement status
- Household location movement (internal migration)
- Leaving system (external migration)
- Leaving study (attrition)
- New household (external migration)
- New household (study recruitment)

Population microsynthesis requires an initial seed. This can be generated by crosstabulating census (or survey) data, depending on the variables being explored.

Combining survey and census data is challenging due to the many ways variables can be defined, especially those relating to behaviours or to household composition. Even the definition of a room differs. This shouldn't affect microsynthesis but will result in slight differences in the results displayed when using a source or another.

## Method
Download [Understanding Society data](https://beta.ukdataservice.ac.uk/datacatalogue/series/series?id=2000053)

Overview of files   
Check how many households are present during the entire survey   
List of household ids for each individual (unnecessary as this already exists in cross wave data files)    
Tracking an individual over time (e.g. employment status)    
List of useful variables in each file      
No location variable other than region    
What are the triggers that change a household?    
What is the stability of households over time? (how many remain the same)    
Computationally intensive to check all individual transitions -> look at distributions for now    

Use 'household_distributions.py' to obtain counts of the required variable    
I then save these counts on excel, normalise to account for decrease in total housholds, and plot the distributions.   
Also added correlations between each variable. Household size and composition is the pair with the highest correlation, r=0.72, folowed by number of bedrooms and rooms (that aren't bedrooms), r=0.55.

All distributions seem to remain constant over time within a small error (<1%).    
Compare survey to census data.
Download census data from [Nomisweb](https://www.nomisweb.co.uk).
Distributions are the same for survey and census for the variables tested.
It is hard to compare certain variables because of the definitions - see [mapping](#mapping-survey-to-census)

5 dimensions required to create a population seed:

-tenure     
-number of rooms    
-number of occupants    
-number of bedrooms     
-household composition      

Counts of each 5-dimensional state using 'crosstabulation.py'. One table per wave.    
Definitions of variables are different to those in census so need to remap the data.    
note: reading in wave f produces a pandas warning due to mixed types in columns (395,396,399,400), these columns are dates and are not used in the crosstabulation so just ignore. 

There is still a diference between rooms in survey and census even after mapping. Perhaps the remap is not possible as it requires information we do not have, however, the distributions are quite close. It is just important to keep the different definitions in mind when look at any outputs produced by the data. 

Constraints: make it impossible to occupy non-sensical states such as 3 people living in a 1 person household.    
This is different from inprobable states. There is a high number of unoccupied states in the seed. Need to give these states a small occupation to differentitate from impossible states. 

option to add dwelling type but variable is stored in a different file (hhsamp instead of hhresp) so will make code slower.    
make sure column order is same as that in household_microsynth    
column names changed for hhsize and counts to avoid problems when calling due to pre existing functions 'size' and 'count'.    

### Mapping Survey to Census

The categories and definitions used to describe households differ between survey and census data. This means it a remapping of data is needed in order to compare between both sources, as well as to use programmes initially made for census inputs.

The first step is to filter the negative values. These are codes for "missing" (-9), "inapplicable" (-8) etc. and need to be dropped before any further preprocessing. This is especially important when combining data because artificial values could be created. For example, to determine the total number of rooms in a house we could add the bedrooms (e.g. -9 bedrooms) and other rooms (e.g. 10 rooms) in a house, however, one of the two values could be missing thus the sum will be erroneous (-9 + 10 = 1 total rooms). 

The census gives the total number of rooms in a household, whilst the survey gives the number of rooms excluding bedrooms. Therefore,  a new column, _rooms_, must be generated by adding bedrooms, _hsbeds_, and other rooms, _hsrooms_.

Only four categories of tenure are used in [household_microsynth](https://github.com/nismod/household_microsynth) from the seven available in survey data:

|Census              | Understanding Society                          |
|--------------------|------------------------------------------------|
|Owned outright      | Owned outright                                 |
|Owned with mortgage | Owned with mortgage                            |
|Rented social       | Local authority rent + Housing associated rent |
|Rented private      | Rented private Unfurnished + Furnished + Other |

A more complex mapping is needed for household composition as the categories don't exactly match:

|Census             | Understanding Society                                              |
|-------------------|--------------------------------------------------------------------|
|Single occupancy   | 1 male, aged 65+; 1 female, age 60+; 1 adult under pensionable age |
|Single parent      | 1 adult, 1 child; 1 adult, 2 or more children                      |
|Married couple*    | Couple under pensionable age, no children; Couple 1 or more over pensionable age, no children; Couple with 1 child; Couple with 3 or more children; 3 or more adults, 1-2 children, incl. at least one couple
|Cohabiting couple* | Couple with 2 children; 3 or more adults, no children, incl. at least one couple; 3 or more adults, >2 children, incl. at least one couple
|Mixed              | 2 adults, not a couple, one or more over pensionable age, no children; 2 adults, not a couple, 1 or more children; 2 adults, not a couple, 1 or more children; 3 or more adults, no children, excl. any couples; 3 or more adults, 1 or more children, excl any couples

<sub><nowiki>*<nowiki> Understanding Society doesn't differentiate between married and cohabiting couples in the _hhtype_ variable thus not possible to match accurately. Could combine and reduce categories by one.
    
The survey gives values for each individual but the census gives distributions. In the case of sizes, these are capped, thus the same needs to be done to survey data, with the final number n being interpreted as n or more:

-rooms cap at 6   
-bedrooms cap at 4   
-occupants cap at 4   

Room and bedroom sizes are also shifted by subtracting one from all values bigger than 1. This is because the census considers values of zero bedrooms to be equal to one bedrooms. 
