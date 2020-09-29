FROM python:3.6-slim
WORKDIR /code_tweet
COPY requirements.txt /code_tweet
ADD . /code_tweet
RUN pip install --trusted-host pypi.python.org -r requirements.txt
CMD ["python", "tweet_collector.py"]