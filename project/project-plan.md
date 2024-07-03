# Project Plan

## Title

Impact of Climate Change: Analysis of Global Carbon Dioxide Levels and Surface Temperature Changes

## Main Question

1. How has climate change influenced global carbon dioxide levels in the atmosphere and surface temperature changes over time?
   
## Description

This project investigates the impact of climate change on global carbon dioxide levels and surface temperature changes, aiming to explain their interconnected dynamics. Using datasets on World Monthly Atmospheric Carbon Dioxide Concentrations and Annual Surface Temperature Change, the study explores temporal trends and potential correlations between these critical climate indicators. By employing advanced statistical techniques, the analysis seeks to uncover patterns, anomalies, and potential causal links influenced by climate change. Insights gleaned from this investigation could contribute to a deeper understanding of climate change's effects on atmospheric carbon dioxide concentrations and surface temperature changes, informing policy-making efforts aimed at mitigating its adverse impacts.

## Datasources

### Datasource1:

* Data: https://climatedata.imf.org/datasets/9c3764c0efcc4c71934ab3988f219e0e/explore
* Data URL:    https://services9.arcgis.com/weJ1QsnbMYJlCHdG/ArcGIS/rest/services/Indicator_3_2_Climate_Indicators_Monthly_Atmospheric_Carbon_Dioxide_concentrations/FeatureServer/0/query?where=1=1&outFields=*&f=geojson
* Data Type: GeoJSON

This dataset presents the concentration of carbon dioxide in the atmosphere on a monthly and yearly basis, dating back to 1958.

### Datasource2:

* Data: https://climatedata.imf.org/datasets/4063314923d74187be9596f10d034914/explore
* Data URL:
https://services9.arcgis.com/weJ1QsnbMYJlCHdG/ArcGIS/rest/services/Indicator_3_1_Climate_Indicators_Annual_Mean_Global_Surface_Temperature/FeatureServer/0/query?where=1=1&outFields=*&f=geojson
* Data Type: GeoJSON

This dataset presents the mean surface temperature change during the period 1961-2023, using temperatures between 1951 and 1980 as a baseline.

## Work Packages

1. Data Acquisition and Initial Setup
* Objective: Set up project infrastructure and acquire necessary datasets.
* Tasks:
    - Task 1.1: Download datasets on CO2 concentrations and surface temperature changes.

2. Development of Data Pipeline
* Objective: Build and test an automated data pipeline for preprocessing the data.
* Tasks:
    - Task 2.1: Write Python scripts for downloading, cleaning, and preprocessing data.
    - Task 2.2: Create pipeline.sh to automate the execution of the data pipeline script.
    - Task 2.3: Store preprocessed data in the /data directory in an appropriate format.

3. Data Analysis and Reporting
* Objective: Analyze the cleaned data and prepare an initial data report.
* Tasks:
    - Task 3.1: Perform exploratory and statistical data analysis.
    - Task 3.2: Generate visualizations and initial findings.
    - Task 3.3: Compile findings into a data-report.pdf detailing the data sources, pipeline, and preliminary results.

4. Automated Testing and CI Integration
* Objective: Ensure data pipeline reliability and automation via continuous integration.
* Tasks:
    - Task 4.1: Write automated tests for the data pipeline.
    - Task 4.2: Create tests.sh to execute the system tests.
    - Task 4.3: Set up GitHub Actions to run tests on every push to the main branch.

5. Final Analysis and Report Development
* Objective: Conduct in-depth analysis and develop the final project report.
* Tasks:
    - Task 5.1: Continue detailed data analysis focusing on identifying trends, anomalies, and potential causal links.
    - Task 5.2: Develop the final project report analysis-report.pdf using insights from the analysis.
