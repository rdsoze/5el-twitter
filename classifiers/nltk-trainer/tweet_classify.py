import nltk.data
import json
import sys

classifier = nltk.data.load("classifiers/corpora/twitter_NaiveBayes.pickle")

def processFile( file_path ,classifier):
  correct   = 0
  wrong     = 0
  json_file = open(file_path)
  while 1:
    line1=json_file.readline()
    if not line1:
      break
    try:
      print line1
      json_data=json.loads(line1)
      if json_data['sentiment'] == "positive":
        sentiment = "positive"
      if json_data['sentiment'] == "negative":
        sentiment = "negative"
      if json_data['sentiment'] == "neutral":
        sentiment = "neutral"
        pass

      words = json_data['tweet'].split(' ') 
      feats = dict([(word, True) for word in words])
      #print feats
      categor = classifier.classify(feats)
      print categor + ":"+sentiment


      if categor == sentiment:
        correct = correct + 1
      else:
        wrong   = wrong   + 1

    except ValueError:
       r=1
    except RuntimeError:
       k=1
  print "Rightly classified: " + str(correct)
  print "Wrongly classified: " + str(wrong)
  print "Total classified: " + str(wrong+correct)

def batchClassify(json_arr):
   json_data=json.loads(json_arr)
   for key, value in json_data.iteritems():
      print key,value 


def classify(input_str):
   words = input_str.split(' ') 
   feats = dict([(word, True) for word in words])
   categor = classifier.classify(feats)
   return categor


if __name__ == "__main__":
  processFile(sys.argv[1],classifier)
