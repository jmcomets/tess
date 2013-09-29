#! /usr/bin/env ruby

require 'json'

if ARGV.length != 1
  $stderr << "usage: #{__FILE__} /path/to/es_output.json\n"
  exit 1
end

ES_output = JSON.parse(File.read(ARGV[0]))

requests = []
ES_output['hits']['hits'].each do |hit|
  requests << {
    "action" => "addObject",
    "body" => hit["_source"]
  }
end

puts({ "requests" => requests }.to_json)
