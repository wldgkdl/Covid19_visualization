# Covid19_visualization

### Description
In this project, I'm going to analyze Covid19 data and visualize it over FLASK web application. \
Also, the data will be updated automatically in FLASK model which means it can reflect all the new data from CDC(Centers for Disease Control and Prevention).

### Environment
Mac

### Prerequisite
Python 3.7 \
Geopandas \
FLASK

### Folders
EDA: With Covid19 30,000,000 record, I preprocessed data depending on our needs and reduced data size from 4GB to 3MB. Also provides some exploratory data analysis. 


Live_DB_pipeline: I reduced the original 4GB CSV file to a 3MB CVS file with data preprocessing. In the future, I want to update the preprocessed CVS file automatically by getting new data from CDC developer API.

USmap_Video_visualization: In addition to the graphical Covid19 data dashboard, I also want to provide video data visualization.

