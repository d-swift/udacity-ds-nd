# Capstone Project: Starbucks Offer Completion

<p align="center">
<img src="img/mike-kenneally-coffee-unsplash.jpg">
</p>
<p align="center">
Credit: Mike Kenneally
</p>

## Blog Post

A medium blog post can be found [here.](https://medium.com/@daniel.swift/udacity-capstone-starbucks-data-8513c26dc1d3)

## Project Overview

Once every few days, Starbucks sends out an offer to users of the mobile app. An offer can be merely an advertisement for a drink or an actual offer such as a discount or BOGO (buy one get one free). Some users might not receive any offer during certain weeks. Not all users receive the same offer.

In this project we derive a target label for offer completionfrom event data and combine this with demographic and offer data to predict who will complete and offer sent to them. Every offer has an expiration period, and the same offer may be sent multiple times. This means care must be taken when processing and transforming the data. To add additional complexity an offer may be marked as complete despite    the person never viewing the offer.

## Problem Statement

Offers are sent to people to entice an action. Some people are more likely to respond to offers than others.
 Predict which customers will respond to offers.

#### Evaluation Metric

Since this is a simple binary classification problem accuracy is a suitable metric. There is a slight class imbalance but a benchmarking exercise will provide contextualise the solution performance.

## Result Summary

The headline accuracy scores are as follows:

- Benchmark prediction (predict majority class): 66%
- Logistic Regression: 68%
- Random Forest: 75%
- Random Forest (tuned parameters): 77%

The tuned random forest model achieved an accuracy score of 77% on both the test and training datasets suggesting the model has not been overfit.

Whilst we selected a decision tree over a logistic model a logistic model shouldn't be ruled out. Logistic regression is easy to interpret and very quick to train, one of the reasons a decision tree may outperform a logistic model is due to how decisions trees can effectively create "bins" in the data with branching logic or deal with categories. This means there may be some features (like categories and bins) we can learn fron the random forest model and implement with a logistic model. 


#### Files 

- `img/` contains images used in the blog post
- `blog_post.md` a blog post for less technical readers
- `1_data_preparation.ipynb` Jupyter notebook containing initial data processing and exploration
- `2_model.ipynb` Jupyter notebook containing model selection, benchmarking and evaluation
- `data/` contains raw unprocessed data and processed data created in `1_data_preparation.ipynb` for use in `model.ipynb`

#### Libraries

Requires Python >= 3.7.4

- math
- json
- pandas 
- numpy
- seaborn
- sklearn
- matplotlib