# RPI Major Data Analysis

**Group 15**  
Raymond Chen, Yuxiao He, Florence Wang, Edwin Zhao  
CSCI 4350 - Data Science  
Assignment 2 - Data Collection and Management

## Project Overview

This project analyzes the popularity trends of academic majors at Rensselaer Polytechnic Institute (RPI) over a 10-year period (2014-2024). Our goal is to provide insights for prospective students navigating college major selection by identifying which programs have shown the strongest growth in popularity at RPI.

**Institution Focus**: RPI-specific data (UNITID = 194824)

## Data Sources

All data collected from NCES/IPEDS Completions surveys:
- [2014 Data](https://nces.ed.gov/ipeds/datacenter/data/C2014_A.zip)
- [2015 Data](https://nces.ed.gov/ipeds/datacenter/data/C2015_A.zip)
- [2016 Data](https://nces.ed.gov/ipeds/datacenter/data/C2016_A.zip)
- [2017 Data](https://nces.ed.gov/ipeds/datacenter/data/C2017_A.zip)
- [2018 Data](https://nces.ed.gov/ipeds/datacenter/data/C2018_A.zip)
- [2019 Data](https://nces.ed.gov/ipeds/datacenter/data/C2019_A.zip)
- [2020 Data](https://nces.ed.gov/ipeds/datacenter/data/C2020_A.zip)
- [2021 Data](https://nces.ed.gov/ipeds/datacenter/data/C2021_A.zip)
- [2022 Data](https://nces.ed.gov/ipeds/datacenter/data/C2022_A.zip)
- [2023 Data](https://nces.ed.gov/ipeds/datacenter/data/C2023_A.zip)
- [2024 Data](https://nces.ed.gov/ipeds/datacenter/data/C2024_A.zip)

## Project Structure

```
├── raw_data/              # Original IPEDS data files (read-only)
│   ├── 2014.csv
│   ├── 2015.csv
│   └── ...
├── filtered_data/         # Processed and filtered datasets
├── keys/                  # Data dictionaries and metadata
│   └── major_key.json
│   └── col_key.json
│   └── awlevel_key.json
├── filter.py             # Data filtering script
└── decode_data.py       # Decode degree and major from code to readable format
└── README.md           
```

## Data Management Approach

### Collection Method
Raw data was downloaded directly from NCES/IPEDS as "Awards/degrees conferred by program (6-digit CIP code), award level, race/ethnicity, and gender" files for each year from 2014-2024.

### Processing Pipeline
1. **Raw Storage**: Files stored unchanged in `/raw_data/` with read-only permissions
2. **Filtering**: Python script filters for:
   - UNITID = 194824 (RPI only)
   - AWLEVEL in [3, 5, 7] (Associates, Bachelors, Masters)
   - Relevant columns only
3. **Standardization**: Added year column and calculated within-year completion shares
4. **Output**: Clean datasets saved to `/filtered_data/`

### Key Design Decisions

**Popularity Measurement**: We standardized popularity as within-year share rather than raw counts to enable fair comparison across years with different total graduation numbers.

**Data Provenance**: Clear separation maintained between raw NCES data (their ownership) and our curated analysis artifacts (our ownership with CC BY licensing).

## Data Management Plan Implementation

### What Worked Well

**Physical Data Handling**: The `/raw_data/` → `/filtered_data/` pipeline with read-only raw files successfully preserved data provenance and prevented accidental modifications.

**Data Ownership**: Clear licensing documentation (CC BY for derived works) and attribution blocks eliminated confusion about redistribution rights.

**Knowledge Discovery**: Within-year share calculation solved cross-year comparability issues and enabled meaningful trend analysis despite varying cohort sizes.

### Areas for Improvement

**Persistence**: While raw files were preserved, planned automated backups and cloud synchronization have not yet been implemented, creating single-point-of-failure risk.

**Preliminary Research**: More thorough investigation of source data structure before collection would have better informed our initial data management plan, reducing mid-project adaptations.

**Metadata Collection**: We discovered valuable race and gender metadata not anticipated in the original plan, requiring on-the-fly documentation strategies.

## Future Enhancements

1. **Backup Implementation**: Automated local and cloud backup systems
2. **Expanded Analysis**: Institution-type benchmarking and labor market linkages
3. **Visualization Tools**: Interactive dashboards for trend exploration
4. **Data Validation**: Automated quality checks and anomaly detection

## Attribution

Raw data courtesy of the National Center for Education Statistics (NCES) Integrated Postsecondary Education Data System (IPEDS). Analysis and curation by Group 15.

---

*This project demonstrates practical data management techniques including provenance preservation, reproducible processing pipelines, and appropriate metadata documentation for longitudinal educational data analysis.*