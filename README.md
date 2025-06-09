# SoccerSense Project - Comprehensive Data Collection Framework

## Overview
This project, **SoccerSense**, is a comprehensive soccer analytics platform that integrates multiple data sources, including structured CSV datasets, unstructured video data, and semi-structured JSON files. The primary goal is to address challenges in soccer analytics by providing automated data ingestion, advanced AI-driven analysis, and real-time insights for coaches, analysts, and scouts.
![image](https://github.com/user-attachments/assets/79cb1f26-a7e2-43d2-8541-e0f3353a19fc)

## Final Product
![image](https://github.com/user-attachments/assets/7c90ae25-d9ca-4cca-a060-9d7b304aef50)
This is the demo video and figures: https://drive.google.com/drive/folders/1uwOWW3hrIYRXy-AmMu_Qvts5WWMsAZGZ?usp=share_link


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


## Repository Link
[GitHub Repository](https://github.com/woshimajintao/BDM-Project)

## Author
**Jintao Ma** - Big Data Management and Analytics Master Program

## License
This project is licensed under the MIT License - see the LICENSE file for details.

