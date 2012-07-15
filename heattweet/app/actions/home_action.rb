require 'erb'
class HomeAction < Cramp::Action
  on_start :start
  @@template = ERB.new(File.read(Geotweet::Application.root('app/views/index.erb')))


  def start
    render @@template.result(binding)
    finish
  end
end
