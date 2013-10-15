#run this by doing "ruby generate_ml_input.rb <FOLDER_NAME>"

require 'set'
require 'csv'

#0 = other, 1 = product, 2 = profile
CLASSIFIED_TYPE = ARGV[1] || 1

DATA_FILE = "data.csv"
DATA_TEST_FILE = "data-test.csv"
HEADERS_FILE = "headers.txt"
CLASS_SET = Set.new

`touch #{DATA_FILE}`
`touch #{DATA_TEST_FILE}`
`touch #{HEADERS_FILE}`

class String
  #converts camel case to underscore case
  def underscore
    self.gsub(/::/, '/').
    gsub(/([A-Z]+)([A-Z][a-z])/,'\1_\2').
    gsub(/([a-z\d])([A-Z])/,'\1_\2').
    tr("-", "_").
    downcase
  end
end

#from a word get all the subwords
def get_subwords(word)
  word.underscore.
  gsub("_", " ").
  gsub("-", " ").
  split(" ")
end

#randomly return the file you should write to
def randomized_write_file
  do_split = rand(5)
  write_file = DATA_FILE

  #20% chance of writing to the other file
  if (do_split == 0)
    write_file = DATA_TEST_FILE
  end

  write_file
end

#count of number of classes in a page - one type of data to learn on
def create_class_count_map(file)
  class_map = {}
  text = IO.read(file).force_encoding("ISO-8859-1").encode("utf-8", replace: nil)
  classes = text.scan(/[class|id]="([\w\-\s]+)"/).map { |a| get_subwords(a[0]) }.flatten(1)

  classes.each do |c|
    class_map[c] = class_map[c].nil? ? 1 : class_map[c] + 1
    CLASS_SET.add(c)
  end

  class_map
end

#given a file and map of data, puts the data into the file along with the classified type
def append_data_to_file(file, data_map)

  CSV.open(randomized_write_file(), "ab") do |csv|
    csv << [file.gsub(",", ""), CLASSIFIED_TYPE, data_map.map { |k,v| "#{k}:#{v}" }].flatten(1)
  end
end

#give it a folder and it appends all the data gathered from it into the data file
def generate_ml_inputs(folder_name, is_root=true)
  if File.directory?(folder_name)
    Dir.glob("#{folder_name}/*") do |file|
      next if file == '.' or file == '..'
      if File.directory?(file)
        generate_ml_inputs(file, false)
      else
        #change this if use different data to learn on
        class_map = create_class_count_map(file)
        append_data_to_file(file, class_map)
      end
    end
  else
    #change this if use different data to learn on
    class_map = create_class_count_map(folder_name)
    append_data_to_file(folder_name, class_map)
  end

  #TODO: this should also be abstracted since it only applies when learning by class count
  if is_root
    #when all the data on the class set is gather, write it to the headers file
    to_write = CLASS_SET.to_a.join("\n")

    #if there's already data, append after the existing data
    if (File.size(HEADERS_FILE) != 0)
        to_write = "\n" + to_write
    end

    File.open(HEADERS_FILE, "a") { |file| file.write(to_write) }

    #hacky way of making sure data in HEADERS_FILE is unique and sorted
    `mv #{HEADERS_FILE} temp.txt`
    `sort temp.txt | uniq > #{HEADERS_FILE}`
    `rm temp.txt`
  end
end

if !(ARGV.first)
  puts "please provide the name of the folder containing websites. second argument (defaults to 1) sets is_product boolean"
  exit
end

generate_ml_inputs(ARGV.first)
