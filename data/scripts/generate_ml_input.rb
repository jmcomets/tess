require 'set'
require 'csv'

IS_PRODUCT = ARGV[1] || 1
DATA_FILE = "data.csv"
HEADERS_FILE = "headers.txt"
CLASS_SET = Set.new

`touch #{DATA_FILE}`
`touch #{HEADERS_FILE}`

class String
  def underscore
    self.gsub(/::/, '/').
    gsub(/([A-Z]+)([A-Z][a-z])/,'\1_\2').
    gsub(/([a-z\d])([A-Z])/,'\1_\2').
    tr("-", "_").
    downcase
  end
end

def get_subwords(word)
  word.underscore.
  gsub("_", " ").
  gsub("-", " ").
  split(" ")
end

def generate_ml_inputs(folder_name, is_root)
  Dir.glob("#{folder_name}/*") do |file|
    next if file == '.' or file == '..'
    if File.directory?(file)
      generate_ml_inputs(file, false)
    else
      append_classes_from_file(file)
    end
  end

  if is_root
    File.open(HEADERS_FILE, "a") { |file| file.write("#{CLASS_SET.to_a.join(",")}\n") }
  end
end

def append_classes_from_file(file)
  class_map = {}
  text = IO.read(file).force_encoding("ISO-8859-1").encode("utf-8", replace: nil)
  classes = text.scan(/[class|id]="([\w\-\s]+)"/).map { |a| get_subwords(a[0]) }.flatten(1)

  classes.each do |c|
    class_map[c] = class_map[c].nil? ? 1 : class_map[c] + 1
    CLASS_SET.add(c)
  end

  CSV.open(DATA_FILE, "ab") do |csv|
    csv << [file.gsub(",", ""), IS_PRODUCT, class_map.map { |k,v| "#{k}:#{v}" }].flatten(1)
  end
end

if !(ARGV.first)
  puts "please provide the name of the folder containing websites"
  exit
end

generate_ml_inputs(ARGV.first, true)
