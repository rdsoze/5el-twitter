# require 'active_support/json'
# Cramp::Websocket.backend = :thin
require 'faraday'
require 'open-uri'
require 'json'

class TweetAction < Cramp::Action
  self.transport = :sse
  
  def start
    STREAM.locations(-180,-90,180,90) do |status|
      p 'aa'
      url = URI.encode("http://192.168.221.89/sentiment?q="+status.attrs[:text])
      a = JSON.parse(Faraday.get(url).body)
      render status.attrs[:coordinates].merge(a).to_json
    end
  end

end
