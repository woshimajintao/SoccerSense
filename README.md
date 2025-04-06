# SoccerSense

This paper presents the SoccerSense project architecture, a com-
prehensive soccer analytics platform that integrates diverse data
sources, including structured CSV datasets, unstructured video
data, and semi-structured JSON files. The primary objective
is to address challenges in soccer analytics by providing auto-
mated data ingestion, advanced AI-driven analysis, and real-
time insights for coaches, analysts, and scouts.

![image](https://github.com/user-attachments/assets/26124c78-6bf3-428d-91c1-f939ba7eb358)

To achieve this, I employed Delta Lake for robust data stor-
age and management, leveraging its ACID transactions, schema
enforcement, and time-travel features. I also used Google Cloud
Storage. The landing zone consists of two phases: the Tempo-
ral Landing Zone for rapid data ingestion and initial process-
ing, and the Persistent Landing Zone for long-term storage,
versioning, and accessibility. Metadata management was in-
tegrated throughout the pipeline to ensure data traceability and
governance


