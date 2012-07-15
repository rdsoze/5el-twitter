import json
if __name__ == "__main__":
  json_file=open("/tmp/file1.json") #twitter.json
  while 1:
    line1=json_file.readline()
    if not line1:
      break
    try:
      json_data=json.loads(line1)
      print json_data['created_at']
    except ValueError:
       r=1
