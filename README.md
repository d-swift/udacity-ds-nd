# Udacity Data Science Nanodegree

This repository contains project submissions for the Udacity Data Science Nanodegree.

## Projects 

### 1. Disaster Response App

This project analyzes disaster data from Figure Eight to build a web application that classifies messages that could be used by emergency workers. The focus of this project is building an end-to-end solution as opposed to model performance.

The data contains real messages that were sent during disaster events. 
Messages are cleansed and lemmatized to remove noise and features are represented as a term frequency-inverse document frequency matrix. The model uses Sklearn's MultiOutputClassifier and Logistic Regression to predict message categories.


### 2. London Bicycle Hire Analysis

This project analyses a large cycle-hire dataset to understand where people frequently cycle and why. This project uses BigQuery (via the python client to process large datasets, the Google Maps API to enrich location data and Plotly and Seaborn for visualisation.


### 3. Starbucks Offer Completion Predictions

Once every few days, Starbucks sends out an offer to users of the mobile app. An offer can be merely an advertisement for a drink or an actual offer such as a discount or BOGO (buy one get one free). Some users might not receive any offer during certain weeks. Not all users receive the same offer.

In this project we derive a target label for offer completionfrom event data and combine this with demographic and offer data to predict who will complete and offer sent to them. Every offer has an expiration period, and the same offer may be sent multiple times. This means care must be taken when processing and transforming the data. To add additional complexity an offer may be marked as complete despite the person never viewing the offer. The benchmark accuracy is 66%, we train a Random Forest classifier to achieve 77% accuracy.

### 4. IBM Content Recommendations

This project analyzes user-article interactions on the IBM Watson Studio platform to make content recommendations using similarity measures and matrix factorization.


## Acknowledgements

The projects in this repoistory were completed as part of the Udacity Data Scientist Nanodegree. Some code examples and data were provided by Udacity. 