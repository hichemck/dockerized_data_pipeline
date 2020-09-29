import requests
from sqlalchemy import create_engine
import logging
import pandas as pd
from config import connection_string, WEBHOOK

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='../logs/slack_log.log', filemode='a'
)

engine = create_engine(connection_string, echo=False)

selection = pd.read_sql('SELECT * FROM tweet;', engine)
print(selection)

data = {'text': selection['sentiment'][0]}

requests.post(url=WEBHOOK, json=data)
print('post ok')