import copy
from tweet_classify import classify,batchClassify 
from flask import Flask,request,url_for
app = Flask(__name__)
app.debug=True
#app.run(host='192.168.221.89')
#app.run('0.0.0.0', port=8000)


@app.route("/test")
def test():
	return request.args.get('q') 

@app.route("/sentiment")
def sentiment():
	return "{\"response\": \"" + str(classify(request.args.get('q'))) + "\"}"

@app.route("/sentiments", methods=['POST'])
def sentiments():
	json_obj = copy.deepcopy(request.form)
	print json_obj
	batchClassify(json_obj)	
	return "Received" 


if __name__ == "__main__":
  app.run()

