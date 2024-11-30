# YouTube Viewing History Insights (CS210 Project)
# Made by Elmar Alasgarov(30407)

## Introduction

This project explores personal YouTube viewing history to uncover patterns in video consumption, preferred channels, and how viewing habits evolve over time. By analyzing and visualizing the data, the goal is to reveal trends that provide a deeper understanding of how YouTube content is consumed.

## Purpose / Motivation

The goal of this project is to:
- Analyze personal viewing habits on YouTube, including video genres, frequency of watching, and peak viewing times.
- Identify the most-watched videos and favorite channels.
- Explore how content consumption changes depending on the time of day.
- AObserve shifts in content preferences over time(if possible).

## Data Description

The dataset for this project consists of YouTube viewing history, which has been scraped from my YouTube account page and converted into a CSV file for analysis. Initially, the data was in HTML format, which was parsed and structured into meaningful columns.

- **Source Data**: [YouTube Viewing History (HTML format)](https://https://github.com/ea004/Elmar-youtube/watch_history.html)
- **Processed Data**: The HTML data has been converted into CSV format for easier analysis and manipulation. [YouTube Viewing History (CSV format)](https://https://github.com/ea004/Elmar-youtube/youtube_watch_history.csv)
- **Data Columns**:
  - **Video Title**: The title of the video watched.
  - **Channel Name**: The name of the YouTube channel that uploaded the video.
  - **Watch Date & Time**: The date and time the video was watched.

## Data Preperation/Process

1. **Data Extraction**: 
   - The raw HTML file (`watch_history.html`) is parsed using `BeautifulSoup` to extract relevant data such as video titles, channel names, and timestamps.
   
2. **Data Cleaning**:
   - Data entries with missing or incomplete information are filtered out, ensuring that only valid rows are retained for analysis.

3. **Data Transformation**:
   - The cleaned data is converted into a CSV file (`youtube_watch_history.csv`) with structured columns for easier access and processing.

4. **Data Analysis Preparation**:
   - The processed data is now ready for deeper analysis, including aggregating views by video, channel, or time period.

## Key Insights
This section will include insights derived from the processed data.

## Challenges & Future Directions

### Challenges:
- **Data Gaps**: Some desired data didn't exist.
- **Variable Data Format**: Data format was html so it was hard to properly scrape without missing information.

### Future Directions:
Will fill at the end of the project

## Project Structure

- `watch_history.html`: The raw HTML file containing the YouTube watch history data.
- `youtube_watch_history.csv`: The cleaned and processed CSV file containing the structured viewing history data.
- `ElmarYoutube.ipynb`: Jupyter notebook containing the data analysis and visualization code (if applicable).
