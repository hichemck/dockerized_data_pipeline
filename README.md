# Building a Dockerized Data Pipeline for Sentiment Analysis

## Task

In this project I have been using the container technology Docker to build 
a data pipeline that streams tweets from tweeter API, performs sentiment analysis and
posts the results in a slack channel. 



## Work Breakdown
The data pipeline consists of 5 jobes:
- Tweet Collector: extract tweets with Tweepy (API) 
- Mongo DB: Load the tweets in a MongoDB
- ETL Job: Extract the tweets from MongoDB, perform sentiment analyisis on the tweets
and load the transformed data in a PostgresDB
- PostGres DB: Load the tweets and their respective sentiment assessment in a Postgres database
- Extract the data from the PostgresDB and load it in a slack channel with a slackbot