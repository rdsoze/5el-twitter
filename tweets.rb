require 'em-twitter'
require 'json'

options = {
  :path   => '/1/statuses/sample.json',
  :oauth  => {
    :consumer_key     => 'FN7fld7Pqd4kSTnIXQqTQ',
    :consumer_secret  => 'gyae5kJeR9T8hTGCpwECrg2T2e0XF68hfKM9UhkuhfQ',
    :token            => '63049749-anYndpmyG9dwtWSwqXvodf25VQErFYL4ypTcCmMsI',
    :token_secret     => 'oZMvEdfbPv7SJAd5CYeOtqPxgcr03jAY9ANjAAh0'
  }
}

EM.run do
  client = EM::Twitter::Client.connect(options)
  client.each do |tweet|
    tjson = JSON.parse(tweet)
    p tjson["text"]
  end
end