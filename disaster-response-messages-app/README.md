# Disaster Response Pipeline Project

This project analyzes disaster data from Figure Eight to build a web application that classifies messages that could be used by emergency workers. The focus of this project is building an end-to-end solution as opposed to model performance.

The data contains real messages that were sent during disaster events. 
Messages are cleansed and lemmatized to remove noise and features are represented as a term frequency-inverse document frequency matrix. The model uses Sklearn's MultiOutputClassifier and Logistic Regression to predict message categories.

## Project Components

### 1. Data preparation - `process_data.py`
- Loads the messages and categories datasets
- Merges the two datasets
- Cleans the data
- Stores it in a SQLite database

### 2. ML Pipeline - `train_classifier.py`

- Loads data from the SQLite database
- Splits the dataset into training and test sets
- Builds a text processing and machine learning pipeline
- Trains and tunes a model using GridSearchCV
- Outputs results on the test set
- Exports the final model as a pickle file

### 3. Flask Web App - `run.py`

- Visualizes data with plotly
- Categorises messages entered by a user.

### Running the app

1. Run the following commands in the project's root directory to set up your database and model.

    - To run ETL pipeline that cleans data and stores in database
        `python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db`
    - To run ML pipeline that trains classifier and saves
        `python models/train_classifier.py data/DisasterResponse.db models/classifier.pkl`

2. Run the following command in the app's directory to run the web app.
    `python run.py`

3. Go to http://0.0.0.0:3001/


### Example Screenshots

<p align="center">
<img src="img/disaster-response-project-clf.png">
</p>
<p align="center">
</p>

<p align="center">
<img src="img/disaster-response-project-viz.png">
</p>
<p align="center">
</p>
