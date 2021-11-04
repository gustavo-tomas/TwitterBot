import tweepy
import time
import datetime
from decouple import config

CONSUMER_KEY=config('CONSUMER_KEY')
CONSUMER_SECRET=config('CONSUMER_SECRET')
ACCESS_KEY=config('ACCESS_KEY')
ACCESS_SECRET=config('ACCESS_SECRET')

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

LAST_SEEN = 'last_seen.txt'

def get_last_seen_id(file):
  f_read = open(file, 'r')
  last_seen_id = int(f_read.read().strip())
  f_read.close()
  return last_seen_id

def set_last_seen_id(last_seen_id, file):
  f_write = open(file, 'w')
  f_write.write(str(last_seen_id))
  f_write.close()
  return

def get_days_till_krismas(tweet):
  today = tweet.created_at.date()
  krismas = datetime.date(today.year, 12, 25)
  return str((krismas - today).days)

def reply_to_krismas():
  print('Looking for krismas...')
  last_seen_id = get_last_seen_id(LAST_SEEN)
  tweets = api.search_tweets(q='#krismas', since_id=last_seen_id)
  for tweet in tweets:
    hashtags = tweet.entities.get('hashtags')
    print(str(tweet.id) + ' - ' + tweet.user.screen_name)
    if any(hashtag.get('text') == 'krismas' for hashtag in hashtags):
      days_left = get_days_till_krismas(tweet)
      last_seen_id = tweet.id
      set_last_seen_id(last_seen_id, LAST_SEEN)
      status = '@' + tweet.user.screen_name + ' ' + days_left + ' days till krismas \U0001F563'
      api.update_status(status, in_reply_to_status_id=tweet.id)
      print('responded to ' + tweet.user.screen_name)

while True:
  reply_to_krismas()
  time.sleep(15)