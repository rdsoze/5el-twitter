require "rubygems"
require "bundler"

module Geotweet
  class Application

    def self.root(path = nil)
      @_root ||= File.expand_path(File.dirname(__FILE__))
      path ? File.join(@_root, path.to_s) : @_root
    end

    def self.env
      @_env ||= ENV['RACK_ENV'] || 'development'
    end

    def self.routes
      @_routes ||= eval(File.read('./config/routes.rb'))
    end

    # Initialize the application
    def self.initialize!
    end

  end
end

Bundler.require(:default, Geotweet::Application.env)
Cramp::Websocket.backend = :thin
TweetStream.configure do |config|
  config.consumer_key       = 'FN7fld7Pqd4kSTnIXQqTQ'
  config.consumer_secret    = 'gyae5kJeR9T8hTGCpwECrg2T2e0XF68hfKM9UhkuhfQ'
  config.oauth_token        = '63049749-anYndpmyG9dwtWSwqXvodf25VQErFYL4ypTcCmMsI'
  config.oauth_token_secret = 'oZMvEdfbPv7SJAd5CYeOtqPxgcr03jAY9ANjAAh0'
  config.auth_method        = :oauth
end

STREAM = TweetStream::Client.new
 
# Preload application classes
Dir['./app/**/*.rb'].each {|f| require f}
