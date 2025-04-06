As each CSV file was processed using PySpark’s DataFrame API, relevant metadata was extracted, including:

\begin{itemize}
    \item \textbf{File Name}: The original name of the CSV file.
    \item \textbf{Columns}: A list of all column names present in the DataFrame.
    \item \textbf{Number of Rows}: The total count of rows in the DataFrame, indicating the dataset’s size.
    \item \textbf{Creation Time}: The exact date and time when the file was ingested into the Temporal Landing Zone.
    \item \textbf{Last Modified Time}: The timestamp indicating the last modification date of the original CSV file, providing traceability.
    \item \textbf{Delta Path}: The specific path where the processed data was stored within Delta Lake.
\end{itemize}


