# User Log Analysis

## Overview
This was a “**Rapid exploratory analysis under constraints**”.\
This project analyzes employee login activity using system-generated logs. The goal is to identify patterns in user traffic, detect peak login activity, and provide visual insights into login behavior across financial years.

The analysis processes raw system logs, extracts relevant login events, and generates statistical and visual reports that help understand employee login trends over time.

---

## Problem Statement
The objective of this project is to generate a report that:

1. Considers **only login-related events**.
2. Filters out days with **fewer than 5 logins**.
3. Segments results by **financial year**.
4. Visualizes key metrics including:
   - **Maximum number of unique employee logins per day**
   - **Average daily login count**

---

## Dataset

The project uses two system log datasets.

### Data-1
Contains the following fields:

- Timestamp  
- Session ID  
- Client IP  
- Username  
- Event  
- LoginSessionType  

### Data-2
Contains:

- Timestamp  
- Username  
- Event  

### Data Processing

Both datasets are:

1. Combined into a single dataset
2. Filtered to retain only relevant fields:
   - **Timestamp**
   - **Username**
3. Cleaned and exported into structured formats such as:

- `.csv`
- `.xlsx`

---

## Methodology

The analysis follows a structured workflow:

1. Load and clean the raw log data.
2. Engineer additional features required for analysis.
3. Group data by **date** and calculate **distinct user counts**.
4. Filter out days with **fewer than 5 logins**.
5. Segment the data by **financial year**.
6. Generate visualizations highlighting:
   - Maximum unique logins per day
   - Average daily login counts

### Visualization Design

Plots were designed with the following considerations:

- Y-axis scaled with **equal separation (10 units)**.
- **Annotated markers** for peak login days.
- **Summary statistics** displayed alongside the plots.

---

## Experiments

Several approaches were tested to refine the analysis:

- Different aggregation strategies:
  - Daily
  - Monthly
  - Yearly
- Different filtering thresholds:
  - Login count ≥ 5
  - Login count ≥ 10
- Multiple visualization formats:
  - Line plots
  - Bar charts

---

## Results

The analysis produced the following insights:

- Login activity plots segmented by **financial year**.
- Identification of **peak login days**.
- Computation of **average daily login counts**.
- Traffic insights across:
  - Annual
  - Monthly
  - Daily levels

The code developed during this project can be **reused for similar log analysis tasks**.

---

## Technologies Used

- Python
- pandas
- matplotlib
- seaborn
- re

---

## Deployment

The analysis was implemented using Python and executed through **Jupyter Notebook (`data_analysis.ipynb`)**.

The outputs include:

- Visual reports
- Cleaned datasets
- Statistical summaries for stakeholders

---

## Lessons Learned

Key takeaways from this project:

1. Monitoring user activity is essential for understanding **system usage patterns**.
2. **Standardized visualizations** significantly improve readability.
3. **Business context** is crucial for meaningful log analysis.
4. Effective visualization improves **communication of analytical insights**.
5. Working with real log data strengthened proficiency in **Python data analysis libraries**.

---

## Future Work

Potential improvements include:

- Developing a **real-time dashboard** for login monitoring.
- Implementing **alerts for unusual login patterns**.
- Extending analysis to include:
  - Session duration
  - Failed login attempts

---

## References

- Python Libraries:
  - pandas
  - matplotlib
  - seaborn
  - re
- Internal system log documentation

---

## Note

Due to privacy concerns, the original system logs are not included in this repository.  
Synthetic data can be used to demonstrate the analysis pipeline.
