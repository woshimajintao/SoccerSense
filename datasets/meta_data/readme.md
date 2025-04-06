As each CSV file was processed using PySpark’s DataFrame API, relevant metadata was extracted, including:

- **File Name**: The original name of the CSV file.  
- **Columns**: A list of all column names present in the DataFrame.  
- **Number of Rows**: The total count of rows in the DataFrame, indicating the dataset’s size.  
- **Creation Time**: The exact date and time when the file was ingested into the Temporal Landing Zone.  
- **Last Modified Time**: The timestamp indicating the last modification date of the original CSV file, providing traceability.  
- **Delta Path**: The specific path where the processed data was stored within Delta Lake.  
