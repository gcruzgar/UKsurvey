# UKsurvey

The objective of this project is to visualise the transitions that occur in the microsynthesis of population.  
Understanding Society data is used to complement ONS census data.

For now, the repository is a list of scripts I am using for analysis.

Things to do:
- keep Readme updated
- could use ukcensusapi module to obtain census data
- give examples for every script?
- create python module 

### Understanding Society Dataset

Longitudinal study of the behaviour of ~40,000 households across the UK.

Data can be downloaded from [UK Data Service](https://beta.ukdataservice.ac.uk/datacatalogue/series/series?id=2000053).
    
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

Where w_ is a prefix denoting the wave. The first wave is denoted a, second wave is b etc.    
Individuals have a unique ID (*pidp*), which is persistent throughout the study. Households also have their own ID (*w_hidp*), nonetheless this is wave specific, thus cannot be used to link information across waves. This means an individual's evolution can be tracked over time, but household transitions have an added layer of complexity. 

The largest files are the individual survey responses (**_w_indresp.tab_**). The other group of files of interest are the household response files (**_w_hhresp.tab_**).

|File name |Number of variables*|Description                                           |
|----------|--------------------|------------------------------------------------------|
|w_hhresp  |200-550             | Substantive data from responding households          |
|w_indresp |1300-2900           | Substantive data from responding adults (16+)        |
|w_youth   |120-170             | Substantive data from youth questionnaire (10-15)    |
|w_hhsamp  |50-200              | Data from Address Record File for issued households  |
|w_indall  |100-200             | Household grid data for all persons in household, including children and non responents|
|w_child   |130-350             |Childcare, consents and school information of all children in the household |
|w_ego_alt |  |Kin and other relationships between pairs of individuals in the household|

<nowiki>*<nowiki>Questions asked in the survey changed every year, so the number of variables is inconsistent.

There is another folder with cross wave data. It consists of three files:

|File name |Description                                           |
|----------|------------------------------------------------------|
|xwavedat  | Substantive data from responding households          |
|xivdata   | Substantive data from responding adults (16+)        |
|xwaveid   | Individual and household identifiers across all waves|

There is considerable attrition in this survey, this is partially compensated by introducing new households in each wave, however, there is a net 23% decrease in housholds over the first 7 years.

More information on the survey can be found here: https://www.understandingsociety.ac.uk.

### Census

Data can be obtained directly from [Nomisweb](https://www.nomisweb.co.uk).    
See [UKCensusAPI](https://github.com/virgesmith/UKCensusAPI) for `python` and `R` wrapper.

### Household microsimulation

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


Combining survey and census data is cahllenging due to the many ways variables can be defined, especailly those relating to behaviours or to household composition.  
