# SoccerSense Project 

## Overview
This project, **SoccerSense**, is a comprehensive soccer analytics platform that integrates multiple data sources, including structured CSV datasets, unstructured video data, and semi-structured JSON files. The primary goal is to address challenges in soccer analytics by providing automated data ingestion, advanced AI-driven analysis, and real-time insights for coaches, analysts, and scouts.
![image](https://github.com/user-attachments/assets/79cb1f26-a7e2-43d2-8541-e0f3353a19fc)

### 🌐 1.Data Sources
Here I have used a variety of structured, semi-structured and unstructured data.
#### Kaggle:https://www.kaggle.com/datasets/davidcariboo/player-scores
#### Transfermarkt: https://www.transfermarkt.co.uk/
#### Youtube: https://www.youtube.com/

### 🗂️ 2. Landing Zone
- **Temporal Landing Zone**  
  Stores raw data including:
  - CSVs (match/player stats)
  - JSON (YouTube comments)
  - MP4 (match videos)

- **Persistent Landing Zone**  
  Cleaned data is written using **Delta Lake** to support:
  - ACID-compliant transactional storage
  - Metadata management and schema enforcement



### 🔐 3. Trusted Zone
- **PySpark** is used for:
  - Large-scale data cleaning and consistency checks
  - Video metadata processing
  - Parsing and structuring YouTube comments
- Data is stored in **DuckDB** for in-memory analytics



### 📈 4. Exploitation Zone
- KPIs (Key Performance Indicators) such as player performance and win rates are computed using **PySpark**
- Results are saved in **Parquet** format for downstream consumption



### 🧑‍💻 5. Consumption Zone
A **Streamlit** web application provides:

- 🎥 **Video Detection Module**  
  Uses **YOLOv8** to detect and track players and ball movement

- 💬 **Sentiment Analysis Module**  
  Applies **VADER** to classify YouTube comments by emotional tone

- 📊 **KPI Dashboard Module**  
  Built with **Streamlit + DuckDB**, enabling:
  - CSV upload & table preview
  - Custom SQL querying
  - Dynamic visualization using **Matplotlib**





## Final Product
![image](https://github.com/user-attachments/assets/7c90ae25-d9ca-4cca-a060-9d7b304aef50)
These are the demo videos: 

https://drive.google.com/drive/folders/1uwOWW3hrIYRXy-AmMu_Qvts5WWMsAZGZ?usp=share_link




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

![KPI2](https://github.com/user-attachments/assets/00194bfc-91f4-4313-82b0-c169c9744843)

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

