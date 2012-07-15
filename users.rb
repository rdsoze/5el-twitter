require 'json'
require 'faraday'
require 'pry'
require 'httparty'
require 'open-uri'

i =1
users = {}
file_url = '/home/raison/Downloads/twitter.json'
file = File.open(file_url).read
file.each_line do |t|
  begin
    i +=1
    p i
    tweet = JSON.parse(t)
    handle = tweet["user"]["screen_name"]
    users.has_key?(handle) ? users[handle] +=1 : users[handle] = 1
  rescue
    next
  end
end 

File.open("users.json","w") do |f|
  f << users.to_json
end