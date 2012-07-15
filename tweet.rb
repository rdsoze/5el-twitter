require 'json'
require 'faraday'
require 'pry'
require 'httparty'
require 'open-uri'

i =1
file_url = '/home/raison/Downloads/twitter.json'
file = File.open(file_url).read
File.open("output2.json","w") do |f|
  file.each_line do |t|
    begin
      next if ((i += 1) < 1100)
      tweet = JSON.parse(t)
            
      #Make call to Alchemy APi - 1000 /day
      # url = "http://access.alchemyapi.com/calls/text/TextGetTextSentiment?apikey=5eacee319920e0f5ad62d4abeaeb2e94fe95b941&outputMode=json&text="

      #Make call to ViralHeat - 5000/day
      url = "http://www.viralheat.com/api/sentiment/review.json?api_key=QFzFI9pb1PbE8dTpCP&text="

      resp = HTTParty.get(URI.escape(url+tweet['text']))
      senti = {"tweet" => tweet['text'], "sentiment" => resp["mood"] }
      f << senti.to_json + "\n"
      p "#{i} -- #{resp['mood']}"
    rescue
      next
    end
  end 
end