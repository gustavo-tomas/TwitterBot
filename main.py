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

def reply_to_krismas():
  print('Looking for krismas...')
  last_seen_id = get_last_seen_id(LAST_SEEN)
  mentions = api.mentions_timeline(since_id=last_seen_id)

  for mention in reversed(mentions):
    today = mention.created_at.date()
    krismas = datetime.date(today.year, 12, 25)
    days_left = krismas - today
    print(str(mention.id) + ' - ' + mention.text + ' - ' + str(today))
    
    last_seen_id = mention.id
    set_last_seen_id(last_seen_id, LAST_SEEN)
    if '#krismas' in mention.text.lower():
      print('responding to ' + mention.user.screen_name)
      status = '@' + mention.user.screen_name + ' ' + str(days_left.days) + ' days till krismas \U0001F563'
      api.update_status(status, in_reply_to_status_id=mention.id)

while True:
  reply_to_krismas()
  time.sleep(15)