import tweepy
import time
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
  print('Replying to krismas')
  last_seen_id = get_last_seen_id(LAST_SEEN)
  mentions = api.mentions_timeline()

  for mention in reversed(mentions):
    print(str(mention.id) + ' - ' + mention.full_text)
    last_seen_id = mention.id
    set_last_seen_id(last_seen_id, LAST_SEEN)
    if '#krismas?' in mention.full_text.lower():
      print('responding')
      api.update_status('@' + mention.user.screen_name + 'Testing', mention.id)

while True:
  reply_to_krismas()
  time.sleep(1)