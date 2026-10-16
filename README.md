# Mars Weather Analysis

A Python data analysis project exploring weather observations from NASA's Curiosity rover on Mars.

## Project Overview

This project uses Python and Pandas to inspect, clean, and analyse Mars weather data. Matplotlib is used to visualize atmospheric pressure and temperature patterns.

## Objectives

- Retrieve Mars weather data from NASA's Curiosity weather feed.
- Inspect data types and identify missing values.
- Convert measurement columns to appropriate data types.
- Investigate potentially unusual minimum-temperature readings using a rolling median.
- Visualize atmospheric pressure against solar longitude.
- Calculate and visualize daily temperature range.

## Data Source

NASA Mars Weather API:

https://mars.nasa.gov/rss/api/?feed=weather&category=msl&feedtype=json

The feed provides weather observations from the Curiosity rover. Data availability and values may change between requests.

## Technologies Used

- Python
- Requests
- Pandas
- Matplotlib

## Analysis Performed

### Data Cleaning
- Converted selected measurement columns to numeric types.
- Converted terrestrial dates to datetime values.
- Identified unavailable measurements represented by `"--"`.
- Excluded columns with no usable measurements from the analysis copy.

### Temperature Investigation
Used a 15-row rolling median to flag minimum-temperature readings that differed from the local median by more than 15 degrees. These readings are candidates for investigation, not confirmed errors.

### Visualizations
- Atmospheric pressure versus solar longitude, with pressure averaged at each longitude.
- Daily temperature range, with a 15-row rolling-median trend.

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/harshatentu05-spec/Mars-Weather-Analysis
cd Mars_Analyser
```



### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Run the analysis

```powershell
python explore.py
```

## Limitations

- Some weather fields are unavailable in the retrieved feed.
- A statistical outlier flag does not establish that a measurement is incorrect.
- Smoothed plots help reveal broad patterns but can hide short-term variation.
- Observed patterns should not be treated as proof of a scientific cause without further investigation.

## Future Improvements

- Improve the handling and documentation of missing data.
- Investigate flagged temperature readings against the source data.
- Improve visualization and interpretation of seasonal pressure changes.
- Add a reproducible analysis workflow and example outputs.

## Status

Work in progress — this project is part of my journey in Python, data analysis, and planetary science.
