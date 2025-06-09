# SoccerSense Project - Comprehensive Data Collection Framework

## Overview
This project, **SoccerSense**, is a comprehensive soccer analytics platform that integrates multiple data sources, including structured CSV datasets, unstructured video data, and semi-structured JSON files. The primary goal is to address challenges in soccer analytics by providing automated data ingestion, advanced AI-driven analysis, and real-time insights for coaches, analysts, and scouts.
![image](https://github.com/user-attachments/assets/79cb1f26-a7e2-43d2-8541-e0f3353a19fc)



## Data Sources
Here I have used a variety of structured, semi-structured and unstructured data.
#### Kaggle:https://www.kaggle.com/datasets/davidcariboo/player-scores
#### Transfermarkt: https://www.transfermarkt.co.uk/
#### Youtube: https://www.youtube.com/


## Installation
To run the code for this project, you will need to install several Python packages.

### Main Packages
- **PySpark** - For distributed data processing.
- **Delta Lake** - To enable ACID transactions and schema enforcement with Spark.
- **yt-dlp** - For downloading YouTube videos.
- **Google API Client Library** - For interacting with YouTube Data API.
- **Kaggle API** - For downloading datasets from Kaggle.
- **Duckdb** – An in-process SQL OLAP database optimized for analytics.
- **ultralytics (YOLO)** – For loading pretrained YOLO models (e.g., YOLOv5, YOLOv8).
- **Streamlit** – For building interactive data apps and dashboards.
- **VADER Sentiment (vaderSentiment)** – A lexicon-based sentiment analysis tool.

### Installation Commands
```bash
# Core data processing and storage
pip install pyspark
pip install delta-spark

# YouTube and API interaction
pip install yt-dlp
pip install google-api-python-client

# External data access
pip install kaggle

# Additional analytics tools
pip install duckdb
pip install streamlit
pip install vaderSentiment

# YOLO pretrained models (via Ultralytics)
pip install ultralytics

```

## Usage
### Step 1: Setting Up Delta Lake
Initialize SparkSession with Delta Lake configuration.
```python
from pyspark.sql import SparkSession
from delta import *

builder = SparkSession.builder.appName("SoccerSense") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

spark = configure_spark_with_delta_pip(builder).getOrCreate()
```

### Step 2: Installing Required Packages
Make sure all the required packages are installed as listed above.

### Step 3: Running Data Ingestion Scripts
Refer to the code files provided in the repository for data ingestion processes including:
- Downloading YouTube videos using `yt-dlp`
- Extracting comments via YouTube Data API
- Downloading CSV data from Kaggle
- Storing data in Delta Lake (Temporal and Persistent Landing Zones)

### Step 4: Metadata Management
Metadata for each dataset is extracted and stored as JSON files like [this](https://drive.google.com/file/d/1-bpG7PXG4g9iOmyarzcFx6-lrkD2qp58/view?usp=sharing) for better traceability.

### Step 5: Data Processing and Analysis
Once all the data is stored, you can proceed with further processing and analysis using Spark DataFrames.

## Repository Link
[GitHub Repository](https://github.com/woshimajintao/BDM-Project)

## Author
**Jintao Ma** - Big Data Management and Analytics Master Program

## License
This project is licensed under the MIT License - see the LICENSE file for details.

