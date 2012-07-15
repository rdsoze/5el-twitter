from crm2 import Classifier
import json
import nltk
from nltk.corpus import stopwords

def remove_stopwords(tweet):
  filtered_tweet = [w for w in tweet if not w in stopwords.words('english')]
#  for w in tweet:
#    if w in stopwords.words('english'):
#      filtered_tweet.remove(w)
  return filtered_tweet

def learn( file_path, sentiment ):
  json_file=open(file_path)
  while 1:
    line1=json_file.readline()
    if not line1:
      break
    try:
      json_data=json.loads(line1)
#      print str(json_data['in_reply_to_user_id_str']) +' ' + json_data['text']
#      if not ( str(json_data['in_reply_to_user_id_str']) == "None" ) :
      if json_data['sentiment'] == "positive":
        senti = "good"
      if json_data['sentiment'] == "negative":
        senti = "bad"
      if json_data['sentiment'] == "neutral":
        senti = "neutral"
        pass
      better_string = " ".join( remove_stopwords(json_data['tweet']) )
      c.learn(senti, better_string)
    except ValueError:
       r=1
#      print "json error"

def test_classification( file_path ):
  correct   = 0
  wrong     = 0
  json_file = open(file_path)
  while 1:
    line1=json_file.readline()
    if not line1:
      break
    try:
      json_data=json.loads(line1)
#      print str(json_data['in_reply_to_user_id_str']) +' ' + json_data['text']
#      if not ( str(json_data['in_reply_to_user_id_str']) == "None" ) :
      if json_data['sentiment'] == "positive":
        senti = "good"
      if json_data['sentiment'] == "negative":
        senti = "bad"
      if json_data['sentiment'] == "neutral":
        senti = "neutral"
        pass
      better_string = " ".join(remove_stopwords(json_data['tweet']))
      (categor, a, b) = c.classify(better_string)
      if categor == senti:
        correct = correct + 1
      else:
        wrong   = wrong   + 1

    except ValueError:
       r=1
    except RuntimeError:
       k=1
  print correct
  print wrong
#  print ( correct / (correct + wrong) )


if __name__ == "__main__":
  c = Classifier("good bad")
  learn("test.json","good")
#  learn("/tmp/twitter.bad", "bad" )
#  learn("/tmp/twitter.neutral", "neutral" )
  # perform a simple test
#  print c.categories
#  print categor
#  (categor, a, b) = c.classify(" tough draw for France and Italy. Germany and Portugal may scrap through")
  test_classification("test2.json")
