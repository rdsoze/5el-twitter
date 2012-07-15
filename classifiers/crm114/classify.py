from crm2 import Classifier
import json

def learn( file_path, sentiment ):
  json_file=open(file_path)
  while 1:
    line1=json_file.readline()
    if not line1:
      break
    try:
      json_data=json.loads(line1)
#      print str(json_data['in_reply_to_user_id_str']) +' ' + json_data['text']
      if not ( str(json_data['in_reply_to_user_id_str']) == "None" ) :
        c.learn(sentiment, json_data['text'])
    except ValueError:
       r=1
#      print "json error"

if __name__ == "__main__":
  c = Classifier("good bad neutral")
  learn("/tmp/twitter.good","good")
  learn("/tmp/twitter.bad", "bad" )
  learn("/tmp/twitter.neutral", "neutral" )
  # perform a simple test
  print c.categories
  (categor, a, b) = c.classify("life is sadness")
  print categor
 	
