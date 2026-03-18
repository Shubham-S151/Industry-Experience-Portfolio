# Vehicle Telemetry Data Processing & Analysis

**Project Name:** Vehicle Telemetry Data Processing & Gear Matrix Creation  
**Overview:** This project processes vehicle telemetry data to create gear matrices based on speed and torque. These matrices are used to analyze vehicle performance under various driving conditions and are automatically generated for new vehicles added to the centralized database.

---

## 1. Problem Statement
Vehicle telematics data is highly valuable for assessing vehicle performance but often requires significant processing before it can be analyzed. This project addresses the need for creating gear matrices based on telemetry data, which are then used to evaluate the vehicle’s performance across different speed and torque ranges. The matrices are automatically generated whenever a new vehicle is added to the central database.

---

## 2. Data
- **Type:** Structured telemetry data (vehicle speed, torque, mileage, and gear position)  
- **Source:** Centralized vehicle telemetry data from the company’s AWS Databricks catalog  
- **Preprocessing:** Data is already cleaned and structured by the Data Engineering team, so no further data cleaning is required in this project.

---

## 3. Approach / Methodology
- **Pipeline Steps:**
  1. **Data Import:** Load telemetry data (e.g., speed, torque, mileage) stored in `.parquet` files from the Databricks catalog.
  2. **Feature Engineering:** Create speed and torque bands to categorize the data.
  3. **Matrix Creation:** Compute the total mileage and mileage percentages for each combination of speed and torque bands.
  4. **Result Export:** Export the resulting matrices into Excel format for easy analysis by the R&D team.
  
- **Tools and Platforms:**
  - **Databricks**: Used for creating and deploying jobs and pipelines.
  - **Python**: Used for data processing with `pandas`, `numpy`, and `openpyxl`.
  - **AWS**: The Databricks platform is hosted on AWS.
  - **Jupyter Notebooks**: Users can run the code interactively using Jupyter if they prefer to execute it manually.

---

## 4. Experiments
- **Baseline:** The basic matrix creation process involves calculating mileage for various speed and torque bands.
- **Automated Process:** Whenever a new vehicle is added to the central database, the pipeline automatically triggers and generates the matrices.
- **Tools Used:** 
  - **Databricks**: For running jobs and setting up triggers.
  - **Python (pandas, numpy, openpyxl)**: For processing data and exporting results.
  
---

## 5. Results
- **Metrics:** Mileage values (total and percentage) for each combination of speed and torque, which are key to evaluating vehicle performance.
- **Visuals:** The results are stored in Excel files with two matrices:
  - **`Mileage_values`**: A matrix of mileage for each speed-torque combination.
  - **`Mileage_percentages`**: A matrix showing the percentage of total mileage for each speed-torque combination.
  
  Users can also view the data through a Databricks dashboard created for raw telemetry data.

---

## 6. Deployment (Optional)
- **Automated Process:** This project is deployed on AWS Databricks and is triggered automatically whenever a new vehicle is added to the database.
- **Interactive Execution:** Users can run the code manually using Jupyter notebooks or Python scripts, making it easy for the team to execute as needed.
- **Dashboard:** A dashboard for visualizing raw data and insights is created on Databricks, allowing team members to interact with the data.

---

## 7. Lessons Learned
- **Automation Benefits:** Setting up the pipeline for automatic execution whenever new vehicles are added saves a lot of manual effort and ensures that the latest data is always processed.
- **Working with Databricks:** Databricks' job and pipeline system allowed for seamless integration with the company’s data infrastructure, making the project more scalable and efficient.
- **Collaboration with Data Engineering:** While I didn’t need to perform data cleaning, close collaboration with the Data Engineering team was essential in ensuring that the data was ready for analysis.
- **Effective Data Processing:** Understanding how to group and bin continuous variables like speed and torque made the matrix creation straightforward but powerful for evaluating vehicle performance.

---

## 8. Future Work
- **Advanced Feature Engineering:** Future work could involve integrating additional vehicle metrics (e.g., fuel efficiency, engine load) for more comprehensive analysis.
- **Real-time Processing:** Moving towards real-time analysis of telemetry data for immediate insights into vehicle performance.
- **Cloud Deployment:** Consider deploying the entire pipeline and dashboard in a more accessible cloud environment, such as AWS or Azure, for easier scalability.

---

## 9. References
- **Datasets Used:** Internal company vehicle telemetry dataset (cleaned and structured by Data Engineering).
- **Tools and Frameworks:** Databricks, Python, pandas, numpy, openpyxl.

---

## Code Architecture

The code structure for this project is designed to process vehicle telemetry data, create gear matrices, and export the results. Below is an overview of the architecture:
```raw
Vehicle-Telemetry-Data-Processing/
│
├── config.py                      # Contains file paths and configuration variables (e.g., result_path, template_path)
│
├── data_import.py                 # Handles the loading of telemetry data from `.parquet` files
│   ├── get_files_paths(path)      # Retrieves the file paths for telemetry data files
│   ├── combine_files(paths)      # Combines the data files into a single DataFrame
│   └── get_type(path)            # Returns the file type (e.g., .parquet)
│
├── data_cleaning.py               # Contains functions for data cleaning, conversion, and feature engineering
│   ├── load_file_paths(root_path) # Simulates loading of file paths
│   ├── merge_files(file_list)     # Merges data files into a single DataFrame
│   ├── clean_data(df)             # Cleans and sorts the data
│   ├── convert_dtypes(df)         # Ensures correct data types for columns
│   ├── feature_engineering(df)    # Generates derived features like speed/torque bands
│   └── process_pipeline(root_path, entity_id) # Main pipeline to process data from start to end
│
├── matrix_creation.py             # Creates the gear matrix by binning speed and torque
│   ├── create_gear_matrix(df)     # Defines the bins and labels for speed and torque, then calculates mileage
│
├── main.py                        # Main script that executes the entire pipeline and exports results
│   ├── main()                     # Loads the data, processes it, creates matrices, and exports them
│   └── export_result(data_dict, ...) # Exports the results into an Excel file
│
└── requirements.txt               # Python dependencies for the project (e.g., pandas, numpy, openpyxl)
```
