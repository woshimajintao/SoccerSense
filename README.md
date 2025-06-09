# SoccerSense Project - Comprehensive Data Collection Framework

## Overview
This project, **SoccerSense**, is a comprehensive soccer analytics platform that integrates multiple data sources, including structured CSV datasets, unstructured video data, and semi-structured JSON files. The primary goal is to address challenges in soccer analytics by providing automated data ingestion, advanced AI-driven analysis, and real-time insights for coaches, analysts, and scouts.
![image](https://github.com/user-attachments/assets/79cb1f26-a7e2-43d2-8541-e0f3353a19fc)

My
system architecture was designed to handle structured, semi￾structured, and unstructured football-related data from various
sources such as Kaggle, YouTube APIs, and direct video down￾loads. 

I began by ingesting data into a Temporal Landing Zone,
where raw CSVs, JSON comments, and MP4 videos were stored
temporarily. Using Delta Lake, I transferred the cleaned and
validated data to a Persistent Landing Zone to ensure ACID￾compliant storage with metadata management.

In the Trusted Zone, I employed PySpark for large-scale data
cleaning and consistency validation across player, club, and
match-related tables, as well as for processing video metadata
and parsing YouTube comments. Then the data was stored with
Duckdb.

Cleaned data was then moved into the Exploitation Zone,
where I derived key performance indicators (KPIs) using PyS￾park, and saved them in Parquet format.

For the Consumption Zone, I developed several interactive
modules using Streamlit. The video detection module lever￾aged YOLOv8 to detect players and ball movement. The senti￾ment analysis module used VADER to classify YouTube com￾ments into emotional categories and visualize audience reac￾tions. The dashboard module, built with Streamlit and DuckDB,
supported CSV uploads, in-memory SQL querying, and dy￾namic KPI visualizations using Matplotlib.

This end-to-end pipeline demonstrated a structured data flow
with integrated analytical components, allowing for real-time
interaction, visual insights, and flexible data consumption. It
ensured data quality, scalability, and domain-specific applica￾bility for football tactical and sentiment analysis.


## Final Product
![image](https://github.com/user-attachments/assets/7c90ae25-d9ca-4cca-a060-9d7b304aef50)
These are the demo videos: 

https://drive.google.com/drive/folders/1uwOWW3hrIYRXy-AmMu_Qvts5WWMsAZGZ?usp=share_link


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
- **PyTorch** – PyTorch for deep learning.
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
pip install PyTorch
pip install duckdb
pip install streamlit
pip install vaderSentiment

# YOLO pretrained models (via Ultralytics)
pip install ultralytics

```

## Usage
### Step 1: Clone the repository
```bash
git clone https://github.com/woshimajintao/SoccerSense.git
cd SoccerSense/P2/Final_APP/Consumption\ Zone
```

### Step 2: Installing Required Packages
Make sure all the required packages are installed as listed above.

### Run the Application
Start the main Streamlit app:

```bash
streamlit run main.py
```
This will launch the application in your browser.

## Figures
### KPI Analytics
![image](https://github.com/user-attachments/assets/2f0bc762-7200-4ce2-8b28-d9233e2202d5)

### Video Detection
![Video Detection](https://github.com/user-attachments/assets/95b47eb5-4ca3-4231-98b0-7bd60b55dc15)

### Sentiment Analytics
![Sentiment Analysis](https://github.com/user-attachments/assets/4b6998f9-146a-4c90-8bd1-5609040e3ebb)


## Repository Link
[GitHub Repository](https://github.com/woshimajintao/BDM-Project)

## Author
**Jintao Ma** - Big Data Management and Analytics Master Program

## License
This project is licensed under the MIT License - see the LICENSE file for details.

