import logging
import pandas as pd
from sqlalchemy import create_engine
import pymongo
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from config import connection_string

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s- %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='../logs/log_etl.log', filemode='w'
)

client = pymongo.MongoClient('mongodb://mongodb:27017/')
db = client.twitter 
collection = db.tweets

collection_list = []
for doc in collection.find()[:3] :
    collection_list.append(doc)
print(collection_list)

df = pd.DataFrame(collection_list)
df.drop(columns='_id', inplace=True)

analyzer = SentimentIntensityAnalyzer()

def analyze(text):
    vs = analyzer.polarity_scores(text)
    return str(vs)

df['sentiment'] = df['text'].apply(analyze)

print(df.head())

engine = create_engine(connection_string, echo=False)
print('engine ok')

one_row=df.sample(n=1)
print(one_row)

one_row.to_sql('tweet', engine, if_exists = 'replace', method = 'multi', chunksize=1000)
print('df to sql ok')
